# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SpiderOutcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RegionItem1(scrapy.Item):
    province = Field()
    def get_insert_sql(self):
        insert_sql = 'insert into tab1 (province) values (%s)'
        province = self['province']
        args_tuple = (province)
        return insert_sql,args_tuple

class RegionItem2(scrapy.Item):

    city = Field()
    city_code = Field()
    def get_insert_sql(self):
        insert_sql = 'insert into tab2 (city,city_code) values (%s,%s)'
        city = self['city']
        city_code = self['city_code']
        args_tuple = (city,city_code)
        return insert_sql,args_tuple


class RegionItem3(scrapy.Item):

    town = Field()
    town_code = Field()
    def get_insert_sql(self):
        insert_sql = 'insert into tab3 (town,town_code) values (%s,%s)'
        town = self['town']
        town_code = self['town_code']
        args_tuple = (town,town_code)
        return insert_sql,args_tuple

class RegionItem4(scrapy.Item):

    village = Field()
    village_code = Field()
    def get_insert_sql(self):
        insert_sql = 'insert into tab4 (village,village_code) values (%s,%s)'
        village = self['village']
        village_code = self['village_code']
        args_tuple = (village,village_code)
        return insert_sql,args_tuple


