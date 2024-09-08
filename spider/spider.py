import re
from lxml import etree
import items
import asyncio
import aiohttp

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
data = {
    'name': '18978509108',
    'password': '123456asdfghjkl',
    'remember': 'true',
    'ck': '',
    'ticket': ''
}
session = None


async def create_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()
    return session


async def close_session():
    global session
    if session is not None:
        await session.close()


async def login(login_url='https://accounts.douban.com/j/mobile/login/basic', data=data):
    async with session.post(login_url, data=data) as response:
        if response.status == 200:
            # 登录成功，处理响应
            print(response.text())
            return response


async def get_text(url):
    try:
        async with session.get(url, headers=headers) as resp:
            resp.encoding = 'utf-8'
            resp.raise_for_status()
            return await resp.text()
    except:
        print(url)
        print("访问异常!")


async def get_comments(url):
    """获取一个url下的所有短评  网址输入为https://music.douban.com/subject/***/comments/  形式 \n """
    text = await get_text(url)
    tree = etree.HTML(text)
    num = int(
        re.findall(r'\d+', tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div/div[1]/ul/li[1]/span/text()')[0])[0])
    num = min(num, 500)  # 确保评论数不超过 500
    pages = [page for page in range(0, 200, 20)]  # 修改为实际需要的页码
    urls = get_comments_urls(url, pages)
    tasks = [get_comment(comment_url) for comment_url in urls]  # 创建获取每个评论的任务
    comments_lists = await asyncio.gather(*tasks)
    all_comments = [comment for sublist in comments_lists for comment in sublist]
    return all_comments


async def get_comment(url):
    """获取输入的URL中的所有短评的数据"""
    text = await get_text(url)
    tree = etree.HTML(text)
    comments = tree.xpath('//*[@id="comments"]/div[1]/ul/li/div[2]')
    CommentSet = []
    for comment in comments:
        unprocessed_score = re.findall('\d', comment.xpath('./h3/span[2]/span[1]/@class')[0])
        score = unprocessed_score[0] if unprocessed_score else None
        # comment_length = str(len(comment.xpath('./p/span/text()')[0]))
        vote_count = comment.xpath('./h3/span[1]/span/text()')[0]
        CommentSet.append(items.Comment(score=score, vote_count=vote_count))
    return CommentSet


async def get_reviews(url):
    """获取该url下所有乐评(长评)的数据,并返回Review类的列表"""
    # 甚至豆瓣这有bug,长评数是对不上它返回的网页数据的，有的页只有16条长评，它计算时却按20条计算
    text = await get_text(url)
    tree = etree.HTML(text)
    num = int(re.findall('\d+', tree.xpath('//*[@id="content"]/h1/text()')[0])[0])
    num = min(num, 500)
    pages = [page for page in range(0, num, 20)]
    urls = get_reviews_urls(url, pages)
    tasks = [get_review(review_url) for review_url in urls]
    review_lists = await asyncio.gather(*tasks)
    all_reviews = [comment for sublist in review_lists for comment in sublist]
    return all_reviews


async def get_review(url):
    """获取当前url下的乐评"""
    text = await get_text(url)
    tree = etree.HTML(text)
    reviews = tree.xpath('//*[@id="content"]/div/div[1]/div[1]//div[@data-cid]')
    reviewsSet = []
    for review in reviews:
        unprocessed_score = re.findall('\d', review.xpath('./div/header/span[1]/@class')[0])
        if not unprocessed_score:
            score = None
        else:
            score = unprocessed_score[0]
        useful_count, useless_count = review.xpath('./div/div/div[3]/a/span/text()')
        reviewsSet.append(
            items.Review(score=score, useful_count=useful_count.strip() if len(useful_count.strip()) else '0',
                         useless_count=useless_count.strip() if len(useless_count.strip()) else '0'))
    return reviewsSet


def get_comments_urls(url, pages):
    """获取一个短评评论区所需要的所有URL"""
    urls = []
    for page in pages:
        _url = url + '?start={}&limit=20&status=P&sort=new_score'.format(page)
        urls.append(_url)
    return urls


def get_reviews_urls(url, pages):
    """获取一个长评的评论区所需要的所有URL"""
    urls = []
    for page in pages:
        _url = url + '?sort=hotest&start={}'.format(page)
        urls.append(_url)
    return urls


async def get_info_artist(url):
    """获取该url对应的音乐人信息"""
    text = await get_text(url)
    tree = etree.HTML(text)
    name = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/h1/text()')[0]
    img_scr = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/div[1]/div[1]/img/@src')[0]
    profile = tree.xpath('//*[@id="content"]/div/div[1]/section[2]/div[1]/div/p[1]/text()')
    profile = profile[0].strip()
    basic_information = tree.xpath('//*[@id="content"]/div/div[1]/section[1]/div[1]/div[2]/ul/li/span/text()')
    info = []
    for i in range(0, len(basic_information), 2):
        info.append(basic_information[i].strip() + basic_information[i + 1].strip())
    # 获取专辑信息
    creations_url = url + 'creations?sortby=collection&type=musician&role=&format=text'
    creations_text = await get_text(creations_url)
    creations_tree = etree.HTML(creations_text)
    creations_album_urls = creations_tree.xpath('//*[@id="content"]/div/div[1]/div[1]/table/tbody/tr/td[1]/a/@href')
    count = len(creations_album_urls)
    count = min(count, 6)
    creations_album_urls = creations_tree.xpath('//*[@id="content"]/div/div[1]/div[1]/table/tbody/tr/td[1]/a/@href')[
                           0:count]
    tasks = [get_album(comment_url, author=name) for comment_url in creations_album_urls]
    album_lists = await asyncio.gather(*tasks)
    albums = [album for album in album_lists]
    return items.Musician(name, profile, img_scr, info, albums)


async def get_album(url, author):
    """获取当前url数据下的专辑类"""
    text = await get_text(url)
    tree = etree.HTML(text)

    player_elements = tree.xpath('//*[@id="info"]/span/span//text()')
    player = ''.join(i.strip() for i in player_elements)
    player = re.sub("表演者:", '', player)

    img_src = tree.xpath('//*[@id="mainpic"]/span/a/img/@src')[0]
    rating = tree.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()')[0]
    disc = tree.xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/div/ul/li/text()')
    voters_number = tree.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/a/span/text()')[0]
    name = tree.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
    # 获取评论数
    comments_num = re.findall('\d+', tree.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')[0])[0]
    reviews_num = re.findall('\d+', tree.xpath('//*[@id="reviews-wrapper"]/header/h2/span/a/text()')[0])[0]
    # 获取专辑信息
    intro1 = tree.xpath('//*[@id="link-report"]/span[1]/text()')
    intro2 = tree.xpath('//*[@id="link-report"]/span[2]/text()')
    _intro = intro1 if not intro2 else intro2
    intro = []
    for i in _intro:
        intro.append(i.strip())
    info_content = tree.xpath('//*[@id="info"]/text()')
    info_title = tree.xpath('//*[@id="info"]/span/text()')
    info_title.insert(0, '表演者:')
    info_content.insert(0, player)

    info_title = [t.strip() for t in info_title if t.strip()]
    info_content = [c.strip() for c in info_content if c.strip()]
    info = [item for pair in zip(info_title, info_content) for item in pair]

    return items.Album(name=name, rating=rating, disc=disc, img=img_src, comments_num=comments_num,
                       reviews_num=reviews_num,
                       voters_number=voters_number, author=author, basic_info=info, intro=intro, url=url)


async def get_all_data(url):
    """返回音乐人,音乐人对象中包含的所有专辑的短评集合，所有专辑的长评集合"""
    musician = await get_info_artist(url)
    comments_tasks = [get_comments(musician.albums[i].url + 'comments') for i in range(len(musician.albums))]
    reviews_tasks = [get_reviews(musician.albums[i].url + 'reviews') for i in range(len(musician.albums))]
    comments = await asyncio.gather(*comments_tasks)
    reviews = await asyncio.gather(*reviews_tasks)
    return musician, comments, reviews