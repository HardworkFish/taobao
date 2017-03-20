# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

'''import scrapy


class ShopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
'''
# -*- coding: utf-8 -*-



# Define here the models for your scraped items





#类的实例化对象

import scrapy

class ShopItem(scrapy.Item):

    # define the fields for your item here like:

    # name = scrapy.Field()

    title = scrapy.Field()

    link = scrapy.Field()

    price = scrapy.Field()

    comment = scrapy.Field()


    pass