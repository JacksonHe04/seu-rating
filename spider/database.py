db = None

def set_database(database):
    global db
    db = database
    return db
def get_seu_rating():
    """让我们假装有这个函数"""
    return 8

def insert_musician_data(musician):
    with db.cursor() as cursor:
        cursor.execute("INSERT INTO musician(name,image_path,basic_info,introduction) VALUES (%s,%s,%s,%s)",
                       (musician.name,musician.img, ';'.join(musician.basic_info), musician.profile))
        db.commit()
        return cursor.lastrowid

def insert_album_data(album):
    with db.cursor() as cursor:
        seu_rating = get_seu_rating()
        sql = ("INSERT INTO album(title,rating,rating_count,cover_image,disc,author,seu_rating,"
               "long_count,short_count,rating_difference,album_intro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        values = (album.name,album.rating, album.voters_num, album.img, ";".join(album.disc), album.author,seu_rating
                  ,album.comments_num, album.reviews_num, (seu_rating-float(album.rating))/float(album.rating)*100, "".join(album.intro))
        cursor.execute(sql,values)
        db.commit()
        return cursor.lastrowid
def insert_musician_album_data(musician_id,album_id):
    with db.cursor() as cursor:
        sql = "INSERT INTO musician_album(musician_id,album_id) VALUES (%s,%s)"
        values = (musician_id,album_id)
        cursor.execute(sql,values)
        db.commit()

def insert_rating_data(album_id,comments,reviews):
    with db.cursor() as cursor:
        for comment in comments:
            sql = "INSERT INTO rating(album_id,score,likes,length,listened,followers) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (album_id,comment.score,comment.vote_count,0,comment.listened,comment.followers)
            cursor.execute(sql,values)
        db.commit()
        for review in reviews:
            sql = "INSERT INTO rating(album_id,score,likes,length,listened,followers) VALUES (%s,%s,%s,%s,%s,%s)"
            values = (album_id,review.score,int(review.useful_count)-int(review.useless_count),1,review.listened,review.followers)
            cursor.execute(sql,values)
        db.commit()

def insert_data(musician,comments,reviews):
    musician_id = insert_musician_data(musician)
    for i in range(len(musician.albums)):
        album_id = insert_album_data(musician.albums[i])
        insert_musician_album_data(musician_id,album_id)
        insert_rating_data(album_id,comments[i],reviews[i])

def delete_all_data():
    """删除所有数据"""
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM rating")
        cursor.execute("DELETE FROM musician_album")
        cursor.execute("DELETE FROM musician")
        cursor.execute("DELETE FROM album")
        cursor.execute("ALTER TABLE rating AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE musician AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE album AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE musician_album AUTO_INCREMENT = 1")
        db.commit()
def delete_musician_data(musician_id):
    """以音乐人为基点删除所有的音乐人信息，对应专辑及其评论"""
    with db.cursor() as cursor:

        cursor.execute("SELECT album_id FROM musician_album WHERE musician_id = %s",musician_id)
        musician_albums = cursor.fetchall()
        format_strings = ','.join(['%s'] * len(musician_albums))
        cursor.execute("DELETE FROM rating WHERE album_id IN (SELECT album_id FROM musician_album WHERE musician_id=%s)", musician_id)
        cursor.execute("DELETE FROM musician_album WHERE musician_id=%s", musician_id)
        cursor.execute(f"DELETE FROM album WHERE id in ({format_strings})", musician_albums)
        cursor.execute("DELETE FROM musician WHERE id=%s", musician_id)
        db.commit()

def delete_album_data(album_id):
    """以专辑为基点删除所有的专辑信息及其评论"""
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM rating WHERE album_id=%s", album_id)
        cursor.execute("DELETE FROM musician_album WHERE album_id=%s", album_id)
        cursor.execute("DELETE FROM album WHERE id=%s", album_id)
        db.commit()