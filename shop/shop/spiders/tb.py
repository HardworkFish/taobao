'''# -*- coding: utf-8 -*-
import scrapy


class TbSpider(scrapy.Spider):
    name = "tb"
    allowed_domains = ["taobao.com"]
    start_urls = ['http://taobao.com/']

    def parse(self, response):
        pass
'''
#

import scrapy
from scrapy.http import Request
import re
from shop.items import ShopItem
#from taobao.items import ShopItem
import urllib
import re#正则表达式
import urllib
class TbSpider(scrapy.Spider):
    name = "tb"#爬虫文件名字
    allowed_domains = ["taobao.com"]#域名
    start_urls = ['http://taobao.com/']
    def parse(self, response):#parse剖析器
        key = '女装'#爬取关键字，用key存储关键字
        for i in range(0, 1):#通过for 循环爬取一个淘宝网站的所有网页
            url = 'https://s.taobao.com/search?q=' + str(key) + '&s=' + str(44*i) #发现网页规律，并构造网址
            #天猫，淘宝的商品的链接网址规律：http：//item.taobao.com/item.htm?id=商品的id
            print(url)
            yield Request(url=url, callback=self.page)
            # 要使爬虫持续下去而不终止则需要使用，yield 而不是 return（yield返回值不终止程序，return返回值终止程序）
        pass
    def page(self, response):
        body = response.body.decode('utf-8','ignore')#平时的网页是utf-8模式，需要经过decode解码，爬取网页body标签里面的所有信息，使用ignore参数忽略爬取失败的情况，避免出错
        pattam_id = '"nid":"(.*?)"'#用正则表达式提取id
        all_id = re.compile(pattam_id).findall(body)
        # print(all_id)
        # print(len(all_id))
        for i in range(0, len(all_id)):
            this_id = all_id[i]
            #num=i

            url = 'https://item.taobao.com/item.htm?id=' + str(this_id)
            yield Request(url=url, callback=self.next)
            pass
        pass
    def next(self, response):
        item = ShopItem()
        # print(response.url)
        url = response.url
        # 获取商品是属于天猫的、天猫超市的、还是淘宝的。
        pattam_url = 'https://(.*?).com'
        subdomain = re.compile(pattam_url).findall(url)
        # print(subdomain)
        # 获取商品的标题
        #print("商品编号", num)
        if subdomain[0] != 'item.taobao': # 判断语句，判断是否为淘宝子域名，标题可以从源代码中取，所以可以用Xpath表达式获取
            title = response.xpath("//div[@class='tb-detail-hd']/h1/text()").extract()#天猫
            pass
        else:
            title = response.xpath("//h3[@class='tb-main-title']/@data-title").extract()#淘宝
            pass
        #淘宝网商品子域名有detail.tmall（天猫），chaoshi.detail.tmall(天猫超市），item.taobao（天猫）
        # print(title)
        item['title'] = title#商品标题
        # 获取商品的链接网址
        item['link'] = url#获取商品链接
        # 获取商品原价格
        if subdomain[0] != 'item.taobao': # 如果不属于淘宝子域名，执行if语句里面的代码
            pattam_price = '"defaultItemPrice":"(.*?)"'#正则表达式
            price = re.compile(pattam_price).findall(response.body.decode('utf-8', 'ignore')) # 天猫
            pass
        else:
            price = response.xpath("//em[@class = 'tb-rmb-num']/text()").extract() # 淘宝
            pass
        # print(price)
        item['price'] = price#商品价格
        # 获取商品的id（用于构造商品评论数量的抓包网址）
        if subdomain[0] != 'item.taobao': # 如果不属于淘宝子域名，执行if语句里面的代码
            pattam_id = 'id=(.*?)&'
            pass
        else:
            # 这种情况（只有上文没有下文）时，使用正则表达式，在最末端用 $ 表示
            pattam_id = 'id=(.*?)$'#"$"匹配字符串末尾
            pass
        this_id = re.compile(pattam_id).findall(url)[0]
        # print(this_id)
        # 构造具有评论数量信息的包的网址，评论数不会出现在网址源代码上，可以通过Fiddler或是F12->network->name->response 找到评论所在的包，找到评论网址
        comment_url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=' + str(this_id)
        # 这个获取网址源代码的代码永远也不会出现错误，因为这个URL的问题，就算URL是错误的，也可以获取到对应错误网址的源代码。
        # 所以不需要使用 try 和 except urllib.URLError as e 来包装。
        comment_data = urllib.request.urlopen(comment_url).read().decode('utf-8', 'ignore')
        pattam_comment = '"rateTotal":(.*?),"'
        comment = re.compile(pattam_comment).findall(comment_data)
        # print(comment)
        item['comment'] = comment


        yield item#返回item对象
