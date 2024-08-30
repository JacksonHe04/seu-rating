import re
import requests
from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor
import item

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    'Cookie':'douban-fav-remind=1; _pk_id.100001.8cb4=b88b267f6c565b8c.1700303588.; __yadk_uid=mqxbKsf0s1jaaXUcMMUb9VPEhL1KTI1g; ll="118309"; bid=_LZMoJ9D-s4; __gads=ID=dbe50ad9a56a1bbb:T=1712897577:RT=1712897577:S=ALNI_MYP8JNZVu83mbPG1iAy8Ueb6Tkq_w; __gpi=UID=00000de9e07290d1:T=1712897577:RT=1712897577:S=ALNI_MYXvJxk8PfQMvECgQl8riKJO1tcSg; __eoi=ID=3de971c59d8ea469:T=1712897577:RT=1712897577:S=AA-Afja5ccZ12-Ue2P4fZDnT2yWr; viewed="35937990_1403307_26949962_36792214"; ct=y; __utmz=30149280.1724944711.16.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1724997430%2C%22https%3A%2F%2Fsearch.douban.com%2Fmusic%2Fsubject_search%3Fsearch_text%3D%E5%91%A8%E6%9D%B0%E4%BC%A6%26cat%3D1003%22%5D; _pk_ses.100001.8cb4=1; __utma=30149280.955162070.1670064800.1724948766.1724997430.18; __utmc=30149280; __utmt=1; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28324; __utmb=30149280.17.10.1724997430; dbcl2="283248144:32vRa3oNrkk"',
}

def get_text(url,headers=None):
    '''得到html数据'''
    try:
        resp=requests.get(url=url,headers=headers)
        resp.encoding='utf-8'
        resp.raise_for_status()
        resp.close()
        return resp.text
    except:
        print("访问异常")
        
url = 'https://music.douban.com/subject/35937990/comments/'
r_url = 'https://music.douban.com/subject/35937990/reviews'

def get_comments(url):
    ''' 获取一个url下的所有短评  网址输入为https://music.douban.com/subject/***/comments/  形式 \n 
    '''
    tree = etree.HTML(get_text(url,headers=headers))
    num = re.findall('\d+',tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div/div[1]/ul/li[1]/span/text()')[0])
    pages = [page for page in range(0,40,20)]
    urls = get_urls(url,pages)
    CommentSet = []
    with ThreadPoolExecutor(10) as Threads:
        for url in urls:
            _commentSet = Threads.submit(get_comment,url)
            CommentSet.append(_commentSet.result()[::])
    return CommentSet
            

def get_comment(url):
    '''获取输入的URL中的所有短评的数据'''
    tree = etree.HTML(get_text(url,headers=headers))
    comments = tree.xpath('//*[@id="comments"]/div[1]/ul/li/div[2]')
    title = tree.xpath('//*[@id="content"]/h1/text()')
    CommentSet=[]
    for comment in comments:
        score = re.findall('\d+',comment.xpath('./h3/span[2]/span[1]/@class')[0])
        user_name = comment.xpath('./h3/span[2]/a/text()')
        user_href = comment.xpath('./h3/span[2]/a/@href')
        comment_content = comment.xpath('./p/span/text()')
        vote_count = comment.xpath('./h3/span[1]/text()')
        CommentSet.append(item.Comment(score = score,user_name = user_name,user_href = user_href,\
            comment_content = comment_content,vote_count=vote_count))
    return CommentSet

def get_reviews(url):
    '''未完成'''
    tree = etree.HTML(get_text(url,headers=headers))
    num = re.findall('\d+',tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div/div[1]/ul/li[1]/span/text()')[0])
    pages = [page for page in range(0,int(num[0]),20)]
    urls = get_urls(url,pages)
    ReviewSet = []
    with ThreadPoolExecutor(10) as Threads:
        for url in urls:
            _reviewSet = Threads.submit(get_review,url)
            ReviewSet.append(_reviewSet)
    return ReviewSet

def get_review(url):
    '''未完成'''
    tree = etree.HTML(get_text(url,headers))
    reviews = tree.xpath('')
    reviewsSet = []
    for review in reviews:
        score = re.findall('\d+',review.xpath('./div/header/span[1]/@class')[0])
        user_href = review.xpath('./div/header/a[2]/@href')
        user_name = review.xpath('./div/header/a[2]/text()')
        comment_content = ''
        useful_count,useless_count = review.xpath('./div/div/div[3]/a/span/text()')
        reviewsSet.append(item.Review(score = score,user_href=user_href,user_name=user_name,\
            comment_content=comment_content,useful_count=useful_count.strip(),useless_count=useless_count.strip()))
    return reviewsSet

def get_info_artist():
    pass

def get_urls(url,pages):
    '''获取一个评论区所需要的所有URL'''
    urls = []
    for page in pages:
        _url = url + '?start={}&limit=20&status=P&sort=new_score'.format(page)
        urls.append(_url)
    return urls

def  get_all_data(urls):
    '''未完成'''
    pass

