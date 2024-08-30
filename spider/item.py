'''暂时用类存放数据，因为我不知道最后算法要什么，这样方便修改'''
class Comment:
    def __init__(self,score = None,user_name = None,user_id = None,user_href = None,comment_content = None,vote_count=None) :
        self.score=score
        self.user_name = str(user_name)
        self.user_id = str(user_id)
        self.user_href = str(user_href)
        self.vote_count = str(vote_count)
        self.comment_content = str(comment_content)
        
class Review:
    def __init__(self,title = None,score = None,user_name = None,user_id = None,user_href = None,\
        comment_content = None,useful_count = None,useless_count = None) :
        self.title=title
        self.score=score
        self.user_name = user_name
        self.user_id = user_id
        self.user_href = user_href
        self.useful_count = useful_count
        self.useless_count = useless_count
        self.comment_content = comment_content