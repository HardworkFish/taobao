# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
'''
class ShopPipeline(object):
    def process_item(self, item, spider):
        return item
        '''
# -*- coding: utf-8 -*-



# Define your item pipelines here

#

# Don't forget to add your pipeline to the ITEM_PIPELINES setting

# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html




class ShopPipeline(object):
#将得到的信息打入终端
    def process_item(self, item, spider):

        title = item['title'][0]

        link = item['link']

        price = item['price'][0]

        comment = item['comment'][0]

       # print("商品编号",num)

        print('商品名', title)

        print('商品链接', link)

        print('商品原价格', price)

        print('商品评论数', comment)

        print('==========================================================\n')

        return item

