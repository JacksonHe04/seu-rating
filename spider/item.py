'''暂时用类存放数据，因为我不知道最后算法要什么，这样方便修改'''
class Comment:#短评评论
    def __init__(self,score = None,comment_length = None,vote_count=None) :
        self.score=score
        self.vote_count = vote_count#短评评价有用数
        self.comment_length = comment_length#短评长度
        
class Review:
    def __init__(self,score = None,user_name = None,user_href = None,\
        reply_count = None,useful_count = None,useless_count = None) :
        self.score=score
        self.useful_count = useful_count #乐评的有用数
        self.useless_count = useless_count#乐评的无用数
        self.reply_count = reply_count
        
class Alubm:
    def __init__(self,name,rating,indents,img) -> None:
        self.img = img
        self.name = name
        self.indents = indents
        self.rating = rating

class Musician:
    def __init__(self,name,profile,img,basic_info,album) -> None:
        self.name = name
        self.profile = profile
        self.img = img
        self.basic_info = basic_info
        self.album = album