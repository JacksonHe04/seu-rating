# web/models.py
# 定义Django应用中的两个模型类Album和Musician并建立了关联关系。
from django.db import models


class Album(models.Model):
    objects = None
    # musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    # 专辑标题，字符类型，最大长度200
    title = models.CharField(max_length=100)
    # 专辑评分，浮点数类型
    rating = models.FloatField()
    # 评分人数，整数类型
    rating_count = models.IntegerField()
    # 专辑封面图片，图片类型，上传路径为'albums/'
    cover_image = models.ImageField(upload_to='albums/')

    def __str__(self):
        return self.title


class Musician(models.Model):
    # 音乐家姓名，字符类型，最大长度100
    DoesNotExist = None
    objects = None
    name = models.CharField(max_length=100)
    # 音乐家头像，图片类型，上传路径为'musicians/'
    image = models.ImageField(upload_to='musicians/')
    # 音乐家基本信息，文本类型
    basic_info = models.TextField()
    # 音乐家详细介绍，文本类型
    introduction = models.TextField()
    # 音乐家与专辑的多对多关系
    albums = models.ManyToManyField(Album)

    def __str__(self):
        return self.name
