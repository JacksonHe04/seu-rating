# import items
# import spider
# import database
#
# urls = ['https://www.douban.com/personage/35848229/','https://www.douban.com/personage/27203601/',
#         'https://www.douban.com/personage/27480373/','https://www.douban.com/personage/35844048/',
#         'https://www.douban.com/personage/30440052/','https://www.douban.com/personage/27207063/',
#         'https://www.douban.com/personage/35848241/','https://www.douban.com/personage/35847610/',
#         'https://www.douban.com/personage/27568682/','https://www.douban.com/personage/27547792/',
#         'https://www.douban.com/personage/27503475/','https://www.douban.com/personage/27229153/',
#         'https://www.douban.com/personage/27492478/','https://www.douban.com/personage/27223836/',
#         'https://www.douban.com/personage/35847904/','https://www.douban.com/personage/27223796/',
#         'https://www.douban.com/personage/27481638/','https://www.douban.com/personage/27230455/',
#         'https://www.douban.com/personage/35847021/','https://www.douban.com/personage/35847513/',]
# for url in urls:
#     musician,comments,reviews = spider.get_all_data(url)
#     database.insert_data(musician,comments,reviews)
#
# print("all done")

import items
import spider
import database
import asyncio
async def main():
    database.delete_all_data()
    await  spider.create_session()
    urls = ['https://www.douban.com/personage/35848229/', 'https://www.douban.com/personage/27203601/',
            'https://www.douban.com/personage/27480373/', 'https://www.douban.com/personage/35844048/']
    for url in urls:
        musician, comments, reviews = await spider.get_all_data(url)
        database.insert_data(musician, comments, reviews)
    await  spider.close_session()
if __name__ == "__main__":
    # 检查是否在已经运行的事件循环中
    asyncio.run(main())
    print("all done")