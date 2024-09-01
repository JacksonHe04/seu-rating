import re
import requests
from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor
import item
import datetime

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    'Cookie':'douban-fav-remind=1; _pk_id.100001.8cb4=b88b267f6c565b8c.1700303588.; __yadk_uid=mqxbKsf0s1jaaXUcMMUb9VPEhL1KTI1g; ll="118309"; bid=_LZMoJ9D-s4; __gads=ID=dbe50ad9a56a1bbb:T=1712897577:RT=1712897577:S=ALNI_MYP8JNZVu83mbPG1iAy8Ueb6Tkq_w; __gpi=UID=00000de9e07290d1:T=1712897577:RT=1712897577:S=ALNI_MYXvJxk8PfQMvECgQl8riKJO1tcSg; __eoi=ID=3de971c59d8ea469:T=1712897577:RT=1712897577:S=AA-Afja5ccZ12-Ue2P4fZDnT2yWr; viewed="35937990_1403307_26949962_36792214"; ct=y; __utmz=30149280.1724944711.16.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1724997430%2C%22https%3A%2F%2Fsearch.douban.com%2Fmusic%2Fsubject_search%3Fsearch_text%3D%E5%91%A8%E6%9D%B0%E4%BC%A6%26cat%3D1003%22%5D; _pk_ses.100001.8cb4=1; __utma=30149280.955162070.1670064800.1724948766.1724997430.18; __utmc=30149280; __utmt=1; ap_v=0,6.0; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28324; __utmb=30149280.17.10.1724997430; dbcl2="283248144:32vRa3oNrkk"',
}
data ={
    'name' : '18978509108',
    'password' : '123456asdfghjk',
    'remember' : 'true'
}
def login(url):
    session = requests.Session()
    resp = session.get(url,headers = headers)
    if resp.status_code == 200:
        content = resp.content
        print(content)
    session.post(url,headers=headers,data=data)

def get_text(url,headers):
    '''得到html数据,记得加headers'''
    try:
        resp=requests.get(url=url,headers=headers)
        resp.encoding='utf-8'
        resp.close()
        resp.raise_for_status()
        return resp.text
    except:
        print(resp.text)
        file = open("./errorLog.txt",'w')
        current_time = datetime.datetime.now()
        file.write(str(current_time)+'\n')
        file.write(resp.text)
        file.close()
        print("访问异常")
    
def get_comments(url):
    ''' 获取一个url下的所有短评  网址输入为https://music.douban.com/subject/***/comments/  形式 \n 
    '''
    tree = etree.HTML(get_text(url,headers=headers))
    num = re.findall('\d+',tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div/div[1]/ul/li[1]/span/text()')[0])
    pages = [page for page in range(0,1000,20)]#int(num[0])登录不上
    urls = get_comments_urls(url,pages)
    CommentSet = []
    with ThreadPoolExecutor(20) as Threads:
        for url in urls:
            _commentSet = Threads.submit(get_comment,url)
            CommentSet.extend(_commentSet.result())
    return CommentSet
            

def get_comment(url):
    '''获取输入的URL中的所有短评的数据'''
    tree = etree.HTML(get_text(url,headers=headers))
    comments = tree.xpath('//*[@id="comments"]/div[1]/ul/li/div[2]')
    CommentSet=[]
    for comment in comments:
        unprocessed_score = re.findall('\d',comment.xpath('./h3/span[2]/span[1]/@class')[0])
        if not unprocessed_score:
            score = 'NULL'
        else :
            score = unprocessed_score[0]
        comment_length = str(len(comment.xpath('./p/span/text()')[0]))
        vote_count = comment.xpath('./h3/span[1]/span/text()')[0]
        CommentSet.append(item.Comment(score = score,\
            comment_length=comment_length,vote_count=vote_count))
    return CommentSet

def get_reviews(url):
    '''获取该url下所有乐评(长评)的数据,并返回ReviewSet'''
    tree = etree.HTML(get_text(url,headers=headers))
    num = re.findall('\d+',tree.xpath('//*[@id="content"]/h1/text()')[0])
    pages = [page for page in range(0,100,20)]#目前这有bug,有一些乐评被折叠了，但没有办法获得被折叠了多少，所以使用评论总数来爬取会报错
    urls = get_reviews_urls(url,pages)
    ReviewSet = []
    with ThreadPoolExecutor(20) as Threads:
        for url in urls:
            _reviewSet = Threads.submit(get_review,url)
            ReviewSet.extend(_reviewSet.result())
    return ReviewSet

def get_review(url):
    '''获取当前url下的乐评'''
    tree = etree.HTML(get_text(url,headers))
    reviews = tree.xpath('//*[@id="content"]/div/div[1]/div[1]/div')
    reviewsSet = []
    for review in reviews:
        unprocessed_score = re.findall('\d',review.xpath('./div/header/span[1]/@class')[0])
        if not unprocessed_score:
            score = 'NULL'
        else :
            score = unprocessed_score[0]
        useful_count,useless_count = review.xpath('./div/div/div[3]/a/span/text()')
        reply_count = re.findall("\d+",review.xpath('./div/div/div[3]/a[3]/text()')[0])[0]
        reviewsSet.append(item.Review(score = score,useful_count=useful_count.strip() if len(useful_count.strip()) else '0',\
        useless_count=useless_count.strip() if len(useless_count.strip()) else '0',reply_count=reply_count))
    return reviewsSet

def get_info_artist(url):
    '''获取该url对应的所有音乐人信息\n
    返回人物简介,人物图片路径,专辑的URL'''
    resp = get_text(url,headers)
    tree = etree.HTML(resp)
    name = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/h1/text()')[0]
    img_scr = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/div[1]/div[1]/img/@src') [0]
    profile = tree.xpath('//*[@id="content"]/div/div[1]/section[2]/div[1]/div/p[1]/text()')
    profile = re.sub(r'\u3000','',profile[0])
    basic_information = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/div[2]/ul/li/span/text()')
    info = []
    for b_i in basic_information:
        info.append(b_i.strip())
    #获取专辑信息
    creations_url = url +'creations?sortby=collection&type=musician&role=&format=text'
    creations_resp = get_text(creations_url,headers)
    creations_tree = etree.HTML(creations_resp)
    creations_album_urls = creations_tree.xpath('//*[@id="content"]/div/div[1]/div[1]/table/tbody/tr/td[1]/a/@href')[0:3]
    albums = []
    with ThreadPoolExecutor(3) as Threads:
        for _url in creations_album_urls:
            t = Threads.submit(get_album,_url,name)
            albums.append(t.result())
    return item.Musician(name,profile,img_scr,info,albums)


def get_album(url,author):
    '''获取当前url数据下的专辑类'''
    resp = get_text(url,headers)
    tree = etree.HTML(resp)
    img_src = tree.xpath('//*[@id="mainpic"]/span/a/img/@src')[0]
    rating = tree.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    indents = tree.xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/div/ul/li/text()')
    voters_number = tree.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/a/span/text()')[0]
    name = tree.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
    comments_num = re.findall('\d+',tree.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')[0])[0]
    reviews_num = re.findall('\d+',tree.xpath('//*[@id="reviews-wrapper"]/header/h2/span/a/text()')[0])[0]
    
    info_content = tree.xpath('//*[@id="info"]/text()')
    info_title = tree.xpath('//*[@id="info"]/span/text()')
    infoC = []#信息内容
    infoT = []#信息标题
    for c in info_content :
        infoC.append(c.strip())
    for t in info_title:
        infoT.append(t.strip())
    infoT=[x for x in infoT if x]
    infoC=[x for x in infoC if x]
    info = [item for pair in zip(infoT, infoC) for item in pair] 
    return item.Alubm(name=name,rating=rating,indents=indents,img=img_src,comments_num=comments_num,reviews_num=reviews_num,
                 voters_number=voters_number,author=author,basic_info=info)


def get_comments_urls(url,pages):
    '''获取一个短评评论区所需要的所有URL'''
    urls = []
    for page in pages:
        _url = url + '?start={}&limit=20&status=P&sort=new_score'.format(page)
        urls.append(_url)
    return urls

def get_reviews_urls(url,pages):
    '''获取一个乐评的评论区所需要的所有URL'''
    urls = []
    for page in pages:
        _url = url + '?sort=hotest&start={}'.format(page)
        urls.append(_url)
    return urls

def  get_all_data(url):
    '''未完成!!!该函数用于一次调用获取所有数据'''
    pass