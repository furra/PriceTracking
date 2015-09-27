# encoding: utf-8
import scrapy, requests
import json, re

from price_tracking.items import TvItem

class FalabellaTvSpider(scrapy.Spider):
  name = "falabella_tv"
  allowed_domains = ["falabella.com"]
  start_urls = [
      "http://www.falabella.com/falabella-cl/category/cat70043/Televisores"
  ]

  def parse(self, response):
    base_url = "http://www.falabella.com"
    tv_links = response.xpath('//div[@class="cajaLP4x"]//div[@class="quickView"]/a/@href').extract()
    print "%s link elements read." % tv_links

    for link in tv_links:
      tv_link = base_url + link
      print "Scraping %s"%tv_link
      yield scrapy.Request(tv_link, callback=self.parse_tv_info)

    print "Advancing to next page"
    next_page = response.xpath('//div[@id="bul-flecha-derecha"]/a/@href').extract()

    if next_page:
      print "Parsing next page"
      yield scrapy.Request(base_url + next_page[0], callback=self.parse)
    else:
      print "No more pages"

  def parse_tv_info(self, response):
    base_url = "http://www.falabella.com/falabella-cl/browse/productJson.jsp?productId=%s"
    tv_id = response.url.split('/')[-2]
    print "Requesting data for id: %s" % tv_id

    req = requests.get(base_url % tv_id)

    if req.status_code == 200:
      print "Response: 200"
      tv_object = json.loads(req.text)
      if tv_object:
        tv_object = tv_object[0]
        tv_item = TvItem()

        tv_item['url'] = response.url
        tv_item['store_code'] = 'falabella'
        tv_item['internal_code'] = tv_id
        tv_item['price'] = tv_object['NORMAL']
        tv_item['internet_price'] = tv_object['INTERNET']

        match = re.match(r'(\d+)=(\d+)', tv_object['stockLevel'])
        tv_item['stock'] =  match.group(2) if match else '0'

        base_info = response.xpath('//table[@id="tablaFichaT"]')
        tv_item['attributes'] = {}
        tv_item['attributes']['brand'] = tv_object['brand']

        tech = base_info.xpath(u'//th[text()="Tecnología"]/following-sibling::*/text()').extract()
        tv_item['attributes']['technology'] = tech[0] if tech else ''

        resolution = base_info.xpath(u'//th[text()="Resolución"]/following-sibling::*/text()').extract()
        tv_item['attributes']['resolution'] = resolution[0] if resolution else ''

        screen_size = base_info.xpath(u'//th[text()="Tamaño de pantalla"]/following-sibling::*/text()').extract()
        tv_item['attributes']['screen_size'] = screen_size[0] if screen_size else ''

        smart_tv = base_info.xpath(u'//th[text()="Smart TV"]/following-sibling::*/text()').extract()
        tv_item['attributes']['smart_tv'] = smart_tv[0] if smart_tv else ''

        three_d = base_info.xpath(u'//th[text()="3D"]/following-sibling::*/text()').extract()
        tv_item['attributes']['3d'] = three_d[0] if three_d else ''

        return tv_item

      else:
        print "Tv data in request is empty\n%s"%(base_url%tv_id)
        return None