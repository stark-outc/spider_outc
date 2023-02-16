# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from twisted.enterprise import adbapi
from .items import *



class SpiderOutcPipeline:
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DATABASE', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')
        self.dbpool = adbapi.ConnectionPool('pymysql', host=host, db=db,
                                            user=user, passwd=passwd, charset='utf8')
    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_db, item)
        query.addErrback(self.handle_error,item)

    def handle_error(self,failure,item):
        print(u'插入数据失败，原因：{}，错误对象：{}'.format(failure, item))

    def insert_db(self, cursor, item):
        insert_sql,args = item.get_insert_sql()
        cursor.execute(insert_sql,args)