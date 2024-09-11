# 爬虫启动器

import items
import spider
import database
import asyncio


async def main():
    database.delete_all_data()
    await  spider.create_session()
    urls = [
            'https://www.douban.com/personage/27481638/',  # 陶喆
            'https://www.douban.com/personage/27229153/',  # 陈奕迅
            'https://www.douban.com/personage/35848229/',  # 苏打绿
            'https://www.douban.com/personage/27203601/',  # 周杰伦
            'https://www.douban.com/personage/27480373/',  # 孙燕姿
            'https://www.douban.com/personage/35844048/',  # 酷玩
            'https://www.douban.com/personage/30440052/',  # Kendrick
            'https://www.douban.com/personage/35848241/',  # 惘闻
            'https://www.douban.com/personage/35847610/',  # RAD
            'https://www.douban.com/personage/27568682/',  # 华晨宇
            'https://www.douban.com/personage/27547792/',  # 薛之谦
            'https://www.douban.com/personage/27503475/',  # 林俊杰
            'https://www.douban.com/personage/27492478/',  # 吴青峰
            'https://www.douban.com/personage/27223836/',  # Kanye
            'https://www.douban.com/personage/35847904/',  # Beatles
            'https://www.douban.com/personage/27223796/',  # 鲍勃迪伦
            'https://www.douban.com/personage/27230455/',  # 邓紫棋
            'https://www.douban.com/personage/35847021/',  # EXO
            'https://www.douban.com/personage/35847513/',  # ONE OK ROCK
            'https://www.douban.com/personage/27564956/',  # Lana
            'https://www.douban.com/personage/34968611/',  # Billie
            'https://www.douban.com/personage/27475785/',  # Lady Gaga
            'https://www.douban.com/personage/27488081/',  # 汪苏泷
            'https://www.douban.com/personage/27502445/',  # 方大同
            'https://www.douban.com/personage/27495234/',  # 张杰
            'https://www.douban.com/personage/27573573/',  # 毛不易
            'https://www.douban.com/personage/27492662/',  # 李荣浩
            'https://www.douban.com/personage/30380440/',  # 赵雷
            'https://www.douban.com/personage/27565740/',  # 许嵩
            'https://www.douban.com/personage/27250999/',  # 王力宏
            'https://www.douban.com/personage/35160591/',  # 马思唯
            'https://www.douban.com/personage/35717262/',  # 郭顶
            'https://www.douban.com/personage/27492675/',  # 杨宗纬
            'https://www.douban.com/personage/27218255/',  # 张学友
            'https://www.douban.com/personage/27499681/',  # 张悬
            'https://www.douban.com/personage/27210549/',  # 王菲
            'https://www.douban.com/personage/27548801/',  # 蔡依林
            'https://www.douban.com/personage/35848247/',  # 五月天
            'https://www.douban.com/personage/35841533/',  # Beyond
            'https://www.douban.com/personage/35845386/',  # 告五人
            'https://www.douban.com/personage/35848455/',  # 五条人
            'https://www.douban.com/personage/35848286/',  # 重塑
            'https://www.douban.com/personage/35848128/',  # 超级市场
            'https://www.douban.com/personage/35848240/',  # 万青
            'https://www.douban.com/personage/35848572/',  # Ef
            'https://www.douban.com/personage/27572144/',  # 宋冬野
            'https://www.douban.com/personage/35848255/',  # 新裤子
            'https://www.douban.com/personage/35848238/',  # 痛仰
            # 'https://www.douban.com/personage/35848132/',  # 刺猬
            # 'https://www.douban.com/personage/35845811/',  # 盘尼西林
            # 'https://www.douban.com/personage/35848143/',  # 二手玫瑰
            # 'https://www.douban.com/personage/35848133/',  # 达达
            # 'https://www.douban.com/personage/35844488/',  # 大波浪
            # 'https://www.douban.com/personage/35846867/',  # Joyside
            # 'https://www.douban.com/personage/35848195/',  # 木马
            # 'https://www.douban.com/personage/35848220/',  # 声音碎片
            # 'https://www.douban.com/personage/35848221/',  # 声音玩具
            # 'https://www.douban.com/personage/27560519/',  # 周深
            # 'https://www.douban.com/personage/35844618/',  # 房东的猫
            # 'https://www.douban.com/personage/35843178/',  # 丢火车
            # 'https://www.douban.com/personage/27499315/',  # 梁博
            # 'https://www.douban.com/personage/27565112/',  # 胡彦斌
            # 'https://www.douban.com/personage/27404192/',  # 张信哲
            # 'https://www.douban.com/personage/27484739/',  # 蔡健雅
            # 'https://www.douban.com/personage//',  # 凤凰传奇
            # 'https://www.douban.com/personage//',  # 伍佰
            # 'https://www.douban.com/personage//',  # 南征北战
            # 'https://www.douban.com/personage//',  # 音阙诗听
            # 'https://www.douban.com/personage//',  # 时代少年团
            # 'https://www.douban.com/personage//',  # TFBOYS
            # 'https://www.douban.com/personage//',  # 麻园诗人
            # 'https://www.douban.com/personage//',  # GALA
            # 'https://www.douban.com/personage//',  # 蛙池
            # 'https://www.douban.com/personage//',  # 康姆士
            # 'https://www.douban.com/personage//',  # 黑豹乐队
            # 'https://www.douban.com/personage//',  # 脆莓
            # 'https://www.douban.com/personage//',  # 陈楚生
            # 'https://www.douban.com/personage//',  # 古巨基
            # 'https://www.douban.com/personage//',  # 单依纯
            # 'https://www.douban.com/personage//',  # 张碧晨
            # 'https://www.douban.com/personage//',  # 张韶涵
            # 'https://www.douban.com/personage//',  # 梁静茹
            # 'https://www.douban.com/personage//',  # 容祖儿
            # 'https://www.douban.com/personage//',  # 莫文蔚
            # 'https://www.douban.com/personage//',  # 陈粒
            # 'https://www.douban.com/personage//',  # 陈绮贞
            # 'https://www.douban.com/personage//',  # 杨丞琳
            # 'https://www.douban.com/personage//',  # 王心凌
            # 'https://www.douban.com/personage//',  # 张惠妹
            # 'https://www.douban.com/personage//',  # 袁娅维
            # 'https://www.douban.com/personage//',  # 那英
            # 'https://www.douban.com/personage//',  # Justin Bieber
            # 'https://www.douban.com/personage//',  # Charlie Puth
            # 'https://www.douban.com/personage//',  # Bruno Mars
            # 'https://www.douban.com/personage//',  # Alan Walker
            # 'https://www.douban.com/personage//',  # Drake
            # 'https://www.douban.com/personage//',  # Ed Sheeran
            # 'https://www.douban.com/personage//',  # Eminem
            # 'https://www.douban.com/personage//',  # XXXTENTACION
            # 'https://www.douban.com/personage//',  # Troye Sivan
            # 'https://www.douban.com/personage//',  # Adele
            # 'https://www.douban.com/personage//',  # Selena Gomez
            # 'https://www.douban.com/personage//',  # Rihanna
            # 'https://www.douban.com/personage//',  # Sia
            # 'https://www.douban.com/personage//',  # The Chainsmokers
            # 'https://www.douban.com/personage//',  # Imagine Dragons
            # 'https://www.douban.com/personage//',  # Maroon 5
            # 'https://www.douban.com/personage//',  #
            ]
    for url in urls:
        musician, comments, reviews = await spider.get_all_data(url)
        database.insert_data(musician, comments, reviews)
        print(musician.name)
    await  spider.close_session()


if __name__ == "__main__":
    # 检查是否在已经运行的事件循环中
    asyncio.run(main())
    print("all done")
