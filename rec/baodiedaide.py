import pymysql
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
import numpy as np
# from twisted.conch.scripts.conch import conn
from sqlalchemy import update

# 使用 SQLAlchemy 连接数据库
engine = create_engine("mysql+pymysql://root:vsmvpvp10MS@localhost/smr_database")
conn = engine.connect()

# 从数据库中提取数据
query = "SELECT * FROM rating;"
data = pd.read_sql(query, engine)
# 去除没有评分的评论
data_cleaned = data.dropna(subset=['score']).copy()


# 2. 定义初始权重：根据likes和length
def calculate_initial_weight(row):
    weight = row['likes']
    if row['length'] == 1:  # 长评权重大
        weight *= 1.2
    return weight if weight > 0 else 1  # 确保权重不为0


data_cleaned['weight'] = data_cleaned.apply(calculate_initial_weight, axis=1)


# 3. 定义迭代法函数来计算综合评分
def iterative_weighting(df, iterations=10):
    df = df.copy()  # 创建副本，避免警告

    df['weighted_score'] = df['score'] * 2

    for i in range(iterations):
        print(f"迭代第 {i + 1} 次")

        # 计算每个专辑的加权平均分数
        def compute_weighted_score(group):
            if group['weight'].sum() > 0:
                return np.average(group['weighted_score'], weights=group['weight'])
            else:
                return np.nan

        new_weighted_scores = df.groupby('album_id').apply(compute_weighted_score)
        new_weighted_scores = new_weighted_scores.reindex(df['album_id']).reset_index(drop=True)

        # 减少更新幅度
        df['new_weighted_score'] = 0.8 * new_weighted_scores + 0.2 * df['weighted_score']
        df['weighted_score'] = df['new_weighted_score'].fillna(df['weighted_score'])

        print(df[['album_id', 'weighted_score']].drop_duplicates())

    return df


# 4. 执行迭代法计算
data_cleaned = iterative_weighting(data_cleaned, iterations=10)


# 5. 归一化到 10 分制
def normalize_to_10(df):
    df = df.copy()  # 创建副本，避免警告
    # 为了增加得分的可变度，添加一个弹性系数
    scaling_factor = 1

    # 使用百分位数进行归一化
    min_weighted_score = df['weighted_score'].min()
    max_weighted_score = df['weighted_score'].max()

    print(f"最小加权评分: {min_weighted_score}, 最大加权评分: {max_weighted_score}")  # 调试信息

    df['final_score'] = (
            scaling_factor * (df['weighted_score'] - min_weighted_score) / (
            max_weighted_score - min_weighted_score) * 10
    )
    # 防止最终分数超出范围
    df['final_score'] = df['final_score'].clip(0, 10)
    return df


data_cleaned = normalize_to_10(data_cleaned)

# 6. 按 album_id 分组，计算每个专辑的最终评分
final_album_scores = data_cleaned.groupby('album_id')['final_score'].mean().reset_index()

# 从数据库中提取数据
query_musician_album = "SELECT * FROM musician_album;"
data_musician_album = pd.read_sql(query_musician_album, engine)
query_musician = "SELECT * FROM musician;"
data_musician = pd.read_sql(query_musician, engine)
query_album = "SELECT * FROM album;"
data_album = pd.read_sql(query_album, engine)

# 合并数据
merged_data = pd.merge(final_album_scores, data_musician_album, on='album_id')
merged_data = pd.merge(merged_data, data_musician, left_on='musician_id', right_on='id', suffixes=('', '_musician'))
merged_data = pd.merge(merged_data, data_album, left_on='album_id', right_on='id', suffixes=('', '_album'))

# 对每个音乐家按评分降序排序，并选择前三名
top_albums = merged_data.groupby('musician_id').apply(
    lambda x: x.sort_values(by='final_score', ascending=False).head(3)
).reset_index(drop=True)

# 提取所需列
top_albums = top_albums[['musician_id', 'album_id', 'final_score']]

# 创建一个字典来存储每个音乐人的前三张专辑的 album_id
musician_top_albums = {}

for _, row in top_albums.iterrows():
    musician_id = row['musician_id']
    album_id = row['album_id']

    if musician_id not in musician_top_albums:
        musician_top_albums[musician_id] = []

    musician_top_albums[musician_id].append(album_id)

for musician_id, albums in musician_top_albums.items():
    # 确保每个音乐人的专辑有 3 张，若不足则补 None
    while len(albums) < 3:
        albums.append(None)

    # 构建参数化 SQL 语句，避免 SQL 注入风险
    update_query = """
    UPDATE musician 
    SET album1 = :album1, album2 = :album2, album3 = :album3 
    WHERE id = :musician_id;
    """
    conn.execute(text(update_query), {
        'album1': albums[0],
        'album2': albums[1],
        'album3': albums[2],
        'musician_id': musician_id
    })

    # 更新 `Album` 表中的 `seu_rating`
    for album_id in albums:
        if album_id is not None:
            # 获取该专辑的评分
            album_score = top_albums[top_albums['album_id'] == album_id]['final_score'].values[0]

            # 更新 `Album` 表的 `seu_rating` 列
            update_query_album = f"""
                UPDATE album 
                SET seu_rating = {album_score} 
                WHERE id = {album_id};
                """
            conn.execute(text(update_query_album))


# 更新 Album 表中的 seu_rating 为每张专辑的最终评分
for index, row in final_album_scores.iterrows():
    album_id = row['album_id']
    album_score = row['final_score']

    # 更新 Album 表的 seu_rating 列
    update_query_album = f"""
    UPDATE album 
    SET seu_rating = {album_score} 
    WHERE id = {album_id};
    """
    conn.execute(text(update_query_album))


# 从数据库中提取数据
query_album = "SELECT id, seu_rating, rating FROM album;"
data_album = pd.read_sql(query_album, engine)

# 计算 rating_difference
data_album['rating_difference'] = (data_album['seu_rating'] - data_album['rating']) / data_album['rating'] * 100

# 更新 Album 表中的 rating_difference
for index, row in data_album.iterrows():
    album_id = row['id']
    rating_difference = row['rating_difference']

    # 更新 Album 表的 rating_difference 列
    update_query_album = f"""
    UPDATE album 
    SET rating_difference = {rating_difference} 
    WHERE id = {album_id};
    """
    conn.execute(text(update_query_album))


# 确保提交事务
conn.commit()

# 确保提交事务
conn.commit()

# 输出结果
print(top_albums)