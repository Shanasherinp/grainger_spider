# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GraingerItem(scrapy.Item):
    # define the fields for your item here like:
    
    Product_URL = scrapy.Field()
    Title = scrapy.Field()
    Image_URL = scrapy.Field()
    MPN = scrapy.Field()
    Breadcrumb = scrapy.Field()
    Specs = scrapy.Field()
        
