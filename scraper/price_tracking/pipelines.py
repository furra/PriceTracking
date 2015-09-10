# -*- coding: utf-8 -*-
from unidecode import unidecode
from datetime import datetime
from pymongo import MongoClient
import re, hashlib

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FalabellaTvPipeline(object):
  client = MongoClient('127.0.0.1', 27017)
  db = client.price_tracking
  tv_collection = db.televisions

  def process_item(self, item, spider):
    attributes = {
      'brand': item['attributes']['brand'].upper(),
      'technology': unidecode(item['attributes']['technology'].upper()).strip(),
      'resolution': unidecode(item['attributes']['resolution'].upper()).strip(),
      'smart_tv': unidecode(item['attributes']['smart_tv']).lower() == 'si',
      '3d': unidecode(item['attributes']['3d']).lower() == 'si'
    }
    store_info = {
      item['store_code']: {
        'url': item['url']
      }
    }
    match = re.match(r'\d+[.,]?\d*', item['attributes']['screen_size'])
    attributes['screen_size'] = float(match.group().replace(',','.')) if match else 0.0

    #normalize attributes

    code_seed = "%s|%s|%s|%s|%s|%s"%(attributes['3d'],
                                     attributes['brand'],
                                     attributes['resolution'],
                                     attributes['screen_size'],
                                     attributes['smart_tv'],
                                     attributes['technology'])
    code = hashlib.md5(code_seed).hexdigest()

    tv = self.tv_collection.find_one({'code':code})
    #check if code exists
    if tv:
      #add new price history if its different

      result = self.tv_collection.update({'code':code},
                                      {'$set': {
                                        'store_info.'+item['store_code']: {
                                          'url': item['url']
                                        }
                                      }
                                    })

      #add new price if last is different
      last_price = tv['price_history'][item['store_code']][-1]
      if last_price['price'] != item['price']:
        result = self.tv_collection.update({'code':code},
                                        {'$push': {
                                          'price_history.'+item['store_code']: {
                                            'date': datetime.now(),
                                            'price': item['price'],
                                            'internet_price': item['internet_price']
                                          }
                                        }
                                      })
        print "Item updated"
    else:
      #create object
      tv_item = {}
      tv_item['code'] = code
      tv_item['store_info'] = store_info
      tv_item['attributes'] = attributes

      tv_item['availability'] = int(item['stock']) > 0

      tv_item['price_history'] = {
        item['store_code']: [
          {
            'date': datetime.now(),
            'price': item['price'],
            'internet_price': item['internet_price']
          }
        ]
      }
      print "Inserting item"
      self.tv_collection.insert(tv_item)

    return item
