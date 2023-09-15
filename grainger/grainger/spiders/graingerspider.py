import scrapy
from scrapy import Request, FormRequest
import json
from ..items import GraingerItem

class GraingerspiderSpider(scrapy.Spider):
    name = 'graingerspider'
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8",
        "Upgrade-Insecure-Requests" : "1",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }
    api_url = "https://www.grainger.com/experience/pub/api/products/by-id"
    api_headers = {
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
        "Content-Type":"application/json",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        """this request pass main url"""
        start_url = "https://www.grainger.com/category/hardware/braces-and-brackets?categoryIndex=1"
        yield scrapy.Request(start_url, headers=self.headers, callback=self.category_page, dont_filter=True)

    def category_page(self,response):
        """in this request find out each categories link"""
        category_links = response.xpath('//li[@class="_3dXDpA l-hSkF"]/a/@href').extract()
        for category_link in category_links:
            category_link = "https://www.grainger.com" + category_link
            # print(category_link)
            yield Request(category_link, headers=self.headers, callback=self.html_product_list_page, dont_filter=True)
            # break

    def html_product_list_page(self,response):
        """in this find out json data in html tag and loaded json data then find productids and created a dict named form_data """
        json_data = response.xpath('//script[@id="__PRELOADED_STATE__"]/text()').extract_first()
        loaded_json_data = json.loads(json_data)
        product_ids = loaded_json_data['category']['collections'][0]['productIds']

        form_data = {"productIds":product_ids}
        yield FormRequest(self.api_url, headers=self.api_headers, callback= self.api_product_list_page, body = json.dumps(form_data),method = 'POST', dont_filter=True)

    def api_product_list_page(self,response):
        """in this access each product_block in product_list then take product_link in product_block and set a product counter"""
        product_list = response.json()
        product_counter = 0

        for product_block in product_list:
            product_counter += 1
            if product_counter < 101:
                product_link = product_block['productDetailUrl']
                product_link = "https://www.grainger.com" + product_link
                yield Request(product_link, headers=self.headers, callback=self.product_page,dont_filter=True)
                # break
    def product_page(self,response):
        """here we access each product page and find out xpath of each deatils to scrape and yield """
        product_url = response.url.split('?')[0]
        title = response.xpath('//h1[@class="lypQpT"]/text()').extract_first()
        image_url = response.xpath('//div[@class="C9-R6X"]/img/@src').extract_first()
        mpn = response.xpath('//div[@class="vDgTDH"]/dd/text()').extract()[1]
        breadcrumb_list = response.xpath('//li[@class="G1pUBW"]/a/text()').extract()
        breadcrumb = " / ".join(breadcrumb_list)

        table_rows = response.xpath('//div[@class="ZTNukB"]')
        table_dict = {}
        for row in table_rows:
            key = row.xpath('dt/text()').extract_first()
            value = row.xpath('dd/text()').extract_first()
            if key:
                table_dict[key] = value
        yield {
            'Product URL': product_url,
            'Title': title,
            'Image URL': image_url,
            'MPN': mpn,
            'Breadcrumb': breadcrumb,
            'Specs': table_dict,
        }
        




    

       
        
    
        

