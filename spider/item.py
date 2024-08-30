'''暂时用类存放数据，因为我不知道最后算法要什么，这样方便修改'''
class Comment:#短评评论
    def __init__(self,score = None,user_name = None,user_href = None,comment_length = None,vote_count=None) :
        self.score=score
        self.user_name = str(user_name)#用户名称
        self.user_href = user_href#用户个人主页
        self.vote_count = vote_count#短评评价有用数
        self.comment_length = comment_length#短评长度
        
class Review:
    def __init__(self,score = None,user_name = None,user_href = None,\
        reply_count = None,useful_count = None,useless_count = None) :
        self.score=score
        self.user_name = user_name
        self.user_href = user_href
        self.useful_count = useful_count #乐评的有用数
        self.useless_count = useless_count#乐评的无用数
        self.reply_count = reply_count