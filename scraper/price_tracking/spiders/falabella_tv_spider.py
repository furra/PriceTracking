import scrapy
import requests
import json

class FalabellaTvSpider(scrapy.Spider):
  name = "falabella_tv"
  allowed_domains = ["falabella.com"]
  start_urls = [
      "http://www.falabella.com/falabella-cl/category/cat70043/Televisores"
  ]

  def parse(self, response):
    base_url = "http://www.falabella.com/falabella-cl/browse/productJson.jsp?productId=%s"
    print response.xpath('//div[@class="cajaLP4x"]/div/input/@value').extract()
    tv_ids = [tv_id for tv_id in response.xpath('//div[@class="cajaLP4x"]/div/input/@value').extract() if tv_id != '0']
    print "===================="
    print tv_ids
    tv_items = []
    for tv_id in tv_ids:
      get_response = requests.get(base_url%tv_id)
      print "requesting id %s"%tv_id
      if get_response.status_code == 200:
        print "Response: 200"
        tv_object = json.loads(get_response.text)
        if tv_object:
          print tv_object[0]
          #process items