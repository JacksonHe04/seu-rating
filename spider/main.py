import items
import spider
import database
import asyncio
import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="1234567890-=",
    database="WJC_databases"
)
phone_data = {
    'area_code': '+86',
    'number' : '',#输入你的手机号，别用我的
    'analytics': 'analytics_log',
    'ticket': 'tr03YdDx3NFXIpdGgji9am4dJ_WE0EcivSXxn4Bn71-dyCyq-Uhfx4sjGsMyRJXYwxQgUiNqrNXQQbZxcx6UNAH2jeWEdg3U4gPut4PUv7LwXe-AXzU9_k5fwXfb7vk0maQaO9B3Yuu5mFllK-BhJouCkw**',
    'randstr': '@AHD',
    'tc_app_id': '2044348370',
    'code': '',#手机上短信验证码输入位置
    'remember': 'true'
}
#密码登录https://accounts.douban.com/j/mobile/login/basic
#短信登录https://accounts.douban.com/j/mobile/login/verify_phone_code
async def main():
    database.set_database(db)
    database.delete_all_data()
    try:
        await  spider.create_session()
        await  spider.login(login_url='https://accounts.douban.com/j/mobile/login/verify_phone_code',data=
                            phone_data)
        # urls = ['https://www.douban.com/personage/35848229/', 'https://www.douban.com/personage/27203601/',
        #         'https://www.douban.com/personage/27480373/', 'https://www.douban.com/personage/35844048/',
        #         'https://www.douban.com/personage/30440052/',
        #         'https://www.douban.com/personage/35848241/', 'https://www.douban.com/personage/35847610/',            #         'https://www.douban.com/personage/27568682/', 'https://www.douban.com/personage/27547792/',
        #         'https://www.douban.com/personage/27503475/', 'https://www.douban.com/personage/27229153/',
        #         'https://www.douban.com/personage/27492478/', 'https://www.douban.com/personage/27223836/',
        #         'https://www.douban.com/personage/35847904/', 'https://www.douban.com/personage/27223796/',
        #         'https://www.douban.com/personage/27481638/', 'https://www.douban.com/personage/27230455/',
        #         'https://www.douban.com/personage/35847021/', 'https://www.douban.com/personage/35847513/', ]
        urls = ['https://www.douban.com/personage/35848229/']
        for url in urls:
            musician, comments, reviews = await spider.get_all_data(url)
            database.insert_data(musician, comments, reviews)
    finally:
        await  spider.close_session()
if __name__ == "__main__":
    asyncio.run(main())
    print("all done")