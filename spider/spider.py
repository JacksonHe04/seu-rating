import re
import requests
from lxml import etree
from concurrent.futures.thread import ThreadPoolExecutor
import items

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
data ={
    'name' : '18978509108',
    'password' : '123456asdfghjkl',
    'remember' : 'true',
    'ck': '',
    'ticket': ''
}
session = requests.Session()
def login(login_url = 'https://accounts.douban.com/j/mobile/login/basic'):
    """登录豆瓣函数，卧槽真用上了"""
    resp = session.post(login_url,data=data,headers = headers)
    if resp.status_code == 200:
        print(resp.text)

def get_text(url):
    """得到html数据,记得加headers"""
    try:
        resp=session.get(url=url,headers=headers)
        resp.encoding='utf-8'
        resp.close()
        resp.raise_for_status()
        return resp.text
    except:
        print(url)
        print("访问异常")
        print("如果上面的url中start=220那么就说明账号未登录，大概率是因为账号重复登录多次被ban了，"
              "登录需要验证码后一般还要短信验证，所以我就不写通过验证码的代码了")
    
def get_comments(url):
    """获取一个url下的所有短评  网址输入为https://music.douban.com/subject/***/comments/  形式 \n """
    tree = etree.HTML(get_text(url))
    num = int(re.findall('\d+',tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div/div[1]/ul/li[1]/span/text()')[0])[0])
    num = num if num<500 else 500
    pages = [page for page in range(0,num,20)]#登录时爬取的评论数最多为500，未登录时最多200，
    urls = get_comments_urls(url,pages)
    CommentSet = []
    with ThreadPoolExecutor(20) as Threads:
        for url in urls:
            _commentSet = Threads.submit(get_comment,url)
            CommentSet.extend(_commentSet.result())
    return CommentSet
            

def get_comment(url):
    """获取输入的URL中的所有短评的数据"""
    tree = etree.HTML(get_text(url))
    comments = tree.xpath('//*[@id="comments"]/div[1]/ul/li/div[2]')
    CommentSet=[]
    for comment in comments:
        unprocessed_score = re.findall('\d',comment.xpath('./h3/span[2]/span[1]/@class')[0])
        if not unprocessed_score:
            score = None
        else :
            score = unprocessed_score[0]
        comment_length = str(len(comment.xpath('./p/span/text()')[0]))
        vote_count = comment.xpath('./h3/span[1]/span/text()')[0]
        CommentSet.append(items.Comment(score = score,comment_length=comment_length,vote_count=vote_count))
    return CommentSet

def get_reviews(url):
    """获取该url下所有乐评(长评)的数据,并返回ReviewSet"""
    tree = etree.HTML(get_text(url))
    num = int(re.findall('\d+',tree.xpath('//*[@id="content"]/h1/text()')[0])[0])
    num = num if num<500 else 500
    pages = [page for page in range(0,num,20)]#目前这有bug,有一些乐评被折叠了，但没有办法获得被折叠了多少，所以使用评论总数来爬取会报错
    urls = get_reviews_urls(url,pages)
    ReviewSet = []
    with ThreadPoolExecutor(20) as Threads:
        for url in urls:
            _reviewSet = Threads.submit(get_review,url)
            ReviewSet.extend(_reviewSet.result())
    return ReviewSet

def get_review(url):
    """获取当前url下的乐评"""
    tree = etree.HTML(get_text(url))
    reviews = tree.xpath('//*[@id="content"]/div/div[1]/div[1]//div[@data-cid]')
    reviewsSet = []
    for review in reviews:
        unprocessed_score = re.findall('\d',review.xpath('./div/header/span[1]/@class')[0])
        if not unprocessed_score:
            score = None
        else :
            score = unprocessed_score[0]
        useful_count,useless_count = review.xpath('./div/div/div[3]/a/span/text()')
        reviewsSet.append(items.Review(score = score,useful_count=useful_count.strip() if len(useful_count.strip()) else '0',
        useless_count=useless_count.strip() if len(useless_count.strip()) else '0'))
    return reviewsSet

def get_info_artist(url):
    """获取该url对应的音乐人信息"""
    resp = get_text(url)
    tree = etree.HTML(resp)

    name = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/h1/text()')[0]
    img_scr = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/div[1]/div[1]/img/@src') [0]
    profile = tree.xpath('//*[@id="content"]/div/div[1]/section[2]/div[1]/div/p[1]/text()')
    profile = profile[0].strip()
    basic_information = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/div[2]/ul/li/span/text()')
    info = []
    for i in range(0,len(basic_information),2):
        info.append(basic_information[i].strip()+basic_information[i+1].strip())
    #获取专辑信息
    creations_url = url +'creations?sortby=collection&type=musician&role=&format=text'
    creations_resp = get_text(creations_url)
    creations_tree = etree.HTML(creations_resp)
    creations_album_urls = creations_tree.xpath('//*[@id="content"]/div/div[1]/div[1]/table/tbody/tr/td[1]/a/@href')
    count = len(creations_album_urls)
    count = count if count<6 else 6
    creations_album_urls = creations_tree.xpath('//*[@id="content"]/div/div[1]/div[1]/table/tbody/tr/td[1]/a/@href')[0:count]
    albums = []
    with ThreadPoolExecutor(6) as Threads:
        for _url in creations_album_urls:
            t = Threads.submit(get_album,_url,name)
            albums.append(t.result())
    return items.Musician(name,profile,img_scr,info,albums)


def get_album(url,author):
    """获取当前url数据下的专辑类"""
    resp = get_text(url)
    tree = etree.HTML(resp)
    
    player = tree.xpath('//*[@id="info"]/span/span//text()')
    new_player = []
    for i in player:
        new_player.append(i.strip())
    player = ''.join(new_player)
    player = re.sub("表演者:",'',player)
    
    img_src = tree.xpath('//*[@id="mainpic"]/span/a/img/@src')[0]
    rating = tree.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    disc = tree.xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/div/ul/li/text()')
    voters_number = tree.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/a/span/text()')[0]
    name = tree.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
    comments_num = re.findall('\d+',tree.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')[0])[0]
    reviews_num = re.findall('\d+',tree.xpath('//*[@id="reviews-wrapper"]/header/h2/span/a/text()')[0])[0]
    
    intro1 = tree.xpath('//*[@id="link-report"]/span[1]/text()')
    intro2 = tree.xpath('//*[@id="link-report"]/span[2]/text()')
    _intro = intro1 if not intro2 else intro2
    intro = []
    for i in _intro:
        intro.append(i.strip())
    info_content = tree.xpath('//*[@id="info"]/text()')
    info_title = tree.xpath('//*[@id="info"]/span/text()')
    info_title.insert(0,'表演者:')
    info_content.insert(0,player)
    infoC = []#信息内容
    infoT = []#信息标题
    for c in info_content :
        infoC.append(c.strip())
    for t in info_title:
        infoT.append(t.strip())
    infoT=[x for x in infoT if x]
    infoC=[x for x in infoC if x]
    info = [item for pair in zip(infoT, infoC) for item in pair] 
    return items.Album(name=name,rating=rating,disc=disc,img=img_src,comments_num=comments_num,reviews_num=reviews_num,
                 voters_number=voters_number,author=author,basic_info=info,intro=intro,url=url)


def get_comments_urls(url,pages):
    """获取一个短评评论区所需要的所有URL"""
    urls = []
    for page in pages:
        _url = url + '?start={}&limit=20&status=P&sort=new_score'.format(page)
        urls.append(_url)
    return urls

def get_reviews_urls(url,pages):
    """获取一个长评的评论区所需要的所有URL"""
    urls = []
    for page in pages:
        _url = url + '?sort=hotest&start={}'.format(page)
        urls.append(_url)
    return urls

def  get_all_data(url):
    """返回音乐人,音乐人对象中包含的所有专辑的短评集合，所有专辑的长评集合"""
    musician = get_info_artist(url)
    Comments = []
    Reviews = []
    for i in range(len(musician.albums)):
        Comments.append(get_comments(musician.albums[i].url+'comments'))
        Reviews.append(get_reviews(musician.albums[i].url+'reviews'))
    return musician,Comments,Reviews

