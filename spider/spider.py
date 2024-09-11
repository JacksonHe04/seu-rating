import re
from lxml import etree
import items
import asyncio
import aiohttp
import sys

is_login = False

headers = {
    "Cookie" : 'douban-fav-remind=1; _pk_id.100001.8cb4=b88b267f6c565b8c.1700303588.; __yadk_uid=mqxbKsf0s1jaaXUcMMUb9VPEhL1KTI1g; ll="118309"; bid=_LZMoJ9D-s4; __gads=ID=dbe50ad9a56a1bbb:T=1712897577:RT=1712897577:S=ALNI_MYP8JNZVu83mbPG1iAy8Ueb6Tkq_w; __gpi=UID=00000de9e07290d1:T=1712897577:RT=1712897577:S=ALNI_MYXvJxk8PfQMvECgQl8riKJO1tcSg; __eoi=ID=3de971c59d8ea469:T=1712897577:RT=1712897577:S=AA-Afja5ccZ12-Ue2P4fZDnT2yWr; ct=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.28324; _ga_Y4GN1R87RG=GS1.1.1725455165.1.0.1725455165.0.0.0; _ga=GA1.1.955162070.1670064800; viewed="35937990_26393161_26647204_6547562_1403307_26647214_1420204_26949962_36792214"; __utmz=30149280.1725880270.50.15.utmcsr=music.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/35937990/reviews; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1725885833%2C%22https%3A%2F%2Fsearch.douban.com%2Fmusic%2Fsubject_search%3Fsearch_text%3D%E5%91%A8%E6%9D%B0%E4%BC%A6%26cat%3D1003%22%5D; _pk_ses.100001.8cb4=1; __utma=30149280.955162070.1670064800.1725880270.1725885833.51; ap_v=0,6.0; __utmc=30149280; __utmt=1; __utmb=30149280.38.10.1725885833',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
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
        global is_login
        is_login = False


async def login(login_url, data):
    """输入登录地址和对应数据"""
    async with session.post(login_url, data=data) as response:
        if response.status == 200:
            # 登录成功，处理响应
            text = await response.text()
            global is_login
            is_login = True
            print(text)
        else:
            print(f"Login failed with status code: {response.status}")


async def get_text(url):
    """获取对应url下的html文本内容"""
    try:
        async with session.get(url, headers=headers) as resp:
            resp.encoding = 'utf-8'
            resp.raise_for_status()
            return await resp.text()
    except:
        return  None


async def get_comments(url):
    """获取一个url下的所有短评  网址输入为https://music.douban.com/subject/***/comments/  形式 """
    text = await get_text(url)
    tree = etree.HTML(text)
    num = int(
        re.findall(r'\d+', tree.xpath('/html/body/div[3]/div[1]/div/div[1]/div/div[1]/ul/li[1]/span/text()')[0])[0])
    num = min(num, 500) if is_login else 200
    pages = [page for page in range(0, num, 20)]#如果你打算登录就将200改为num
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
        comment_length = str(len(comment.xpath('./p/span/text()')[0] if comment.xpath('./p/span/text()') else []))
        vote_count = comment.xpath('./h3/span[1]/span/text()')[0]
        href = comment.xpath('./h3/span[2]/a/@href')[0]
        followers, listened =  await get_personal_info(href)
        CommentSet.append(items.Comment(score=score, comment_length=comment_length, vote_count=vote_count,
            listened=listened,followers=followers))
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
    reviews_lists = []
    for review in reviews:
        unprocessed_score = re.findall('\d', review.xpath('./div/header/span[1]/@class')[0])
        score = unprocessed_score[0] if unprocessed_score else None
        useful_count, useless_count = review.xpath('./div/div/div[3]/a/span/text()')
        href = review.xpath('./div/header/a/@href')[0]
        followers,listened = await get_personal_info(href)
        reviews_lists.append(items.Review(score=score, useful_count=useful_count.strip() if len(useful_count.strip()) else '0',
                         useless_count=useless_count.strip() if len(useless_count.strip()) else '0',followers=followers,listened=listened))
    return reviews_lists

async def get_personal_info(url):
    """获取该url下的个人信息，返回粉丝数和听过的数量"""
    personal_text = await get_text(url)
    if personal_text is None:
        return None,None
    followers = None
    listened = None
    pattern = r'被(?P<followers>\d+)人关注|(?P<listened>\d+)张听过'
    # 查找所有匹配项
    matches = re.finditer(pattern, personal_text)
    for match in matches:
        # 打印每个匹配项的结果
        if match.group('followers'):
            followers = match.group('followers')
        if match.group('listened'):
            listened = match.group('listened')
    return followers,listened

def convert_arabic_numerals(text):
    """将阿拉伯数字改为标准数字"""
    arabic_to_latin = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
    return text.translate(arabic_to_latin)
def get_comments_urls(url, pages):
    """获取一个短评评论区所需要的所有URL"""
    urls = [url + '?start={}&limit=20&status=P&sort=new_score'.format(page) for page in pages]
    return urls


def get_reviews_urls(url, pages):
    """获取一个长评的评论区所需要的所有URL"""
    urls = [url + '?sort=hotest&start={}'.format(page) for page in pages]
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
    comments_tasks = [get_comments(musician.albums[i].url + 'comments/') for i in range(len(musician.albums))]
    reviews_tasks = [get_reviews(musician.albums[i].url + 'reviews') for i in range(len(musician.albums))]
    comments = await asyncio.gather(*comments_tasks)
    reviews = await asyncio.gather(*reviews_tasks)
    return musician, comments, reviews