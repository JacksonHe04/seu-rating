# import_data.py
# 导入CSV模块和BaseCommand类以及Musician和Album模型
import csv
import os
import sys
import django

from django.conf import settings

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProjectPro.settings')
django.setup()  # 这会初始化 Django 设置和应用注册表

sys.path.append('/Users/jackson/PycharmProjects/BDTrueValueRecSys/djangoProjectPro')

from django.core.management.base import BaseCommand
from djangoProjectPro.smrWeb.models import Musician, Album


# 定义Command类，继承自BaseCommand，用于导入数据
class Command(BaseCommand):
    # 设置help属性，描述命令功能
    help = 'Imports data from CSV files into the database'

    # handle方法用于执行命令，处理数据导入
    def handle(self, *args, **options):
        # 首先导入专辑数据
        self.import_albums()
        # 然后导入音乐家数据
        self.import_musicians()

    # import_albums方法用于从CSV文件中导入专辑数据
    def import_albums(self):
        # 打开专辑数据的CSV文件，使用utf-8编码读取
        with open('../../../zjl_album.csv', mode='r', encoding='utf-8') as file:
            # 使用csv.DictReader读取CSV文件，返回的是一个字典对象
            reader = csv.DictReader(file)
            # 遍历每一行数据，创建Album对象并保存到数据库
            for row in reader:
                Album.objects.create(
                    title=row['title'],
                    rating=row['rating'],
                    rating_count=row['rating_count'],
                    disc=row['disc'],
                    cover_img=row['cover_img']
                )
            # 输出成功导入信息
            self.stdout.write(self.style.SUCCESS('Successfully imported albums'))

    # import_musicians方法用于从CSV文件中导入音乐家数据
    def import_musicians(self):
        # 打开音乐家数据的CSV文件，使用utf-8编码读取
        with open('../../../zjl_musician.csv', mode='r', encoding='utf-8') as file:
            # 使用csv.DictReader读取CSV文件
            reader = csv.DictReader(file)
            # 遍历每一行数据，创建Musician对象并保存到数据库
            for row in reader:
                Musician.objects.create(
                    name=row['name'],
                    img_path=row['img_path'],
                    basic_info=row['basic_info'],
                    introduction=row['introduction']
                )
            # 输出成功导入信息
            self.stdout.write(self.style.SUCCESS('Successfully imported musicians'))
