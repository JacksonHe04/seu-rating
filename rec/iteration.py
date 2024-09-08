import pymysql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# 使用 SQLAlchemy 连接数据库
engine = create_engine("mysql+pymysql://root:root@localhost/bdt_database")
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="bdt_database"
)

cursor = db.cursor()

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


def get_seu_rating():
    try:
        # 将最终评分更新到 album 表中
        for index, row in final_album_scores.iterrows():
            album_id = row['album_id']
            final_rating = row['final_score']
            update_query = f"UPDATE album SET seu_rating = {final_rating} WHERE id = {album_id}"
            cursor.execute(update_query)

        # 提交事务
        db.commit()
    except Exception as e:
        print(f"发生错误: {e}")
        db.rollback()


# 调用函数
get_seu_rating()


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
top_albums = top_albums[['musician_id', 'name', 'title', 'final_score', 'album_id']]


# 更新 musician 表中的排名信息
def show_musician_top_album():
    try:
        # 获取每个音乐家的前三名专辑 ID
        top_albums_grouped = top_albums.groupby('musician_id').head(3)
        top_albums_grouped = top_albums_grouped.sort_values(by=['musician_id', 'final_score'], ascending=[True, False])

        # 更新 musician 表中的 rank1_id, rank2_id, rank3_id
        for musician_id, group in top_albums_grouped.groupby('musician_id'):
            album_ids = group['album_id'].tolist()

            # 使用参数化查询
            update_query = """
                UPDATE musician 
                SET rank1_id = %s, 
                    rank2_id = %s, 
                    rank3_id = %s 
                WHERE id = %s
            """
            cursor.execute(update_query, (
            album_ids[0], album_ids[1] if len(album_ids) > 1 else None, album_ids[2] if len(album_ids) > 2 else None,
            musician_id))

        # 提交事务
        db.commit()
    except Exception as e:
        print(f"发生错误: {e}")
        db.rollback()


# 调用函数
show_musician_top_album()

# 关闭数据库连接
db.close()
# # 将结果插入新表 `recommend`
# top_albums.to_sql('recommend', con=engine, if_exists='append', index=False)
#
# # 输出结果
# print(top_albums)

