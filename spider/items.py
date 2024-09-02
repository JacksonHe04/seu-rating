'''暂时用类存放数据，因为我不知道最后算法要什么，这样方便修改'''
class Comment:
    """短评"""
    def __init__(self,score = None,comment_length = None,vote_count=None) :
        self.score=score #评分
        self.vote_count = vote_count#短评评价有用数
        self.comment_length = comment_length#短评长度
        
class Review:
    """长评"""
    def __init__(self,score = None,useful_count = None,useless_count = None) :
        self.score=score #评分
        self.useful_count = useful_count #乐评的有用数
        self.useless_count = useless_count#乐评的无用数

class Album:
    def __init__(self,name=None,rating=None,basic_info=None,indents=None,url = None,
                 img=None,voters_number=None,comments_num=None,reviews_num=None,author=None) :
        self.img = img #图片路径
        self.name = name #专辑名称
        self.indents = indents#曲目，别问为什么是indent,html中存在这<li class="indent" data-track-order="1.">Intro</li>
        self.rating = rating #评分
        self.voters_num = voters_number #投票人数
        self.author = author #作者
        self.basic_info = basic_info #基础信息
        self.comments_num = comments_num #短评数
        self.reviews_num = reviews_num #长评数
        self.url = url #本专辑对应的url
        
class Musician:
    def __init__(self,name,profile,img,basic_info,album) -> None:
        self.name = name #人名
        self.profile = profile #个人简介
        self.img = img #人物图片
        self.basic_info = basic_info #基础信息
        self.album = album #创作的专辑