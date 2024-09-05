import items
import spider
import database

database.delete_all_data()
urls = ['https://www.douban.com/personage/35848229/','https://www.douban.com/personage/27203601/',
        'https://www.douban.com/personage/27480373/','https://www.douban.com/personage/35844048/']
for url in urls:
    musician,comments,reviews = spider.get_all_data(url)
    database.insert_data(musician,comments,reviews)
print("all done")