import spider
import items
import mysql.connector
import lxml

db = mysql.connector.connect(
    host="localhost",  # MySQL服务器地址
    user="root",  # 用户名
    password="1234567890-=",  # 密码
    database="WJC_databases"  # 数据库名称
)
cursor = db.cursor()
def get_seu_rating():
    """让我们假装有这个函数"""
    return 10

def insert_musician_data(musician):
    cursor.execute("INSERT INTO musician(name,image_path,basic_info,introduction) VALUES (%s,%s,%s,%s)",
                   (musician.name,musician.img, ';'.join(musician.basic_info), musician.profile))
    db.commit()
    return cursor.lastrowid

def insert_album_data(album):
    seu_rating = get_seu_rating()
    sql = ("INSERT INTO album(title,rating,rating_count,cover_image,disc,author,seu_rating,"
           "long_count,short_count,rating_difference,album_intro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    values = (album.name,album.rating, album.voters_num, album.img, ";".join(album.disc), album.author,seu_rating
              ,album.comments_num, album.reviews_num, float(album.rating)-seu_rating, "".join(album.intro))
    cursor.execute(sql,values)
    db.commit()
    return cursor.lastrowid
def insert_musician_album_data(musician_id,album_id):
    sql = "INSERT INTO musician_album(musician_id,album_id) VALUES (%s,%s)"
    values = (musician_id,album_id)
    cursor.execute(sql,values)
    db.commit()

def insert_rating_data(album_id,comments,reviews):
    for comment in comments:
        sql = "INSERT INTO rating(album_id,score,likes,length) VALUES (%s,%s,%s,%s)"
        values = (album_id,comment.score,comment.vote_count,0)
        cursor.execute(sql,values)
    db.commit()
    for review in reviews:
        sql = "INSERT INTO rating(album_id,score,likes,length) VALUES (%s,%s,%s,%s)"
        values = (album_id,review.score,int(review.useful_count)-int(review.useless_count),1)
        cursor.execute(sql,values)
    db.commit()

def insert_data(musician,comments,reviews):
    musician_id = insert_musician_data(musician)
    for i in range(len(musician.albums)):
        album_id = insert_album_data(musician.albums[i])
        insert_musician_album_data(musician_id,album_id)
        insert_rating_data(album_id,comments[i],reviews[i])

def delete_all_data():
    cursor.execute("DELETE FROM rating")
    cursor.execute("DELETE FROM musician_album")
    cursor.execute("DELETE FROM musician")
    cursor.execute("DELETE FROM album")
    cursor.execute("ALTER TABLE rating AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE musician AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE album AUTO_INCREMENT = 1")
    cursor.execute("ALTER TABLE musician_album AUTO_INCREMENT = 1")
    db.commit()