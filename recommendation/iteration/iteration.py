import pymysql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# 使用 SQLAlchemy 连接数据库
engine = create_engine("mysql+pymysql://root:root@localhost/bdt_database")

# 从数据库中提取数据
query = "SELECT * FROM rating;"
data = pd.read_sql(query, engine)
# # 连接数据库
# db_connection = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="bdt_database"
# )
#
# # 从数据库中提取数据
# query = "SELECT * FROM rating;"
# data = pd.read_sql(query, db_connection)
#
# # 关闭数据库连接
# db_connection.close()

# 去除没有评分的评论
data_cleaned = data.dropna(subset=['score']).copy()
# 检查数据
print("数据基本信息：")
print(data_cleaned.info())
print(data_cleaned.head())

# 2. 定义初始权重：根据likes和length
def calculate_initial_weight(row):
    weight = row['likes']
    if row['length'] == 1:  # 长评权重大
        weight *= 1.5
    return weight if weight > 0 else 1  # 确保权重不为0


# # 使用 .loc 明确指定要修改的列，确保修改的是原始数据
# data_cleaned.loc[:, 'weight'] = data_cleaned.apply(calculate_initial_weight, axis=1)
data_cleaned['weight'] = data_cleaned.apply(calculate_initial_weight, axis=1)


# 3. 定义迭代法函数来计算综合评分
def iterative_weighting(df, iterations=10):
    df = df.copy()  # 创建副本，避免警告

    # # 初始时，用 score 作为加权评分的初始值，明确使用 .loc
    # df.loc[:, 'weighted_score'] = df['score']
    df['weighted_score'] = df['score'] * 2

    for i in range(iterations):
        print(f"迭代第 {i + 1} 次")
        # # 按 album_id 分组计算加权平均分数
        # new_weighted_scores = df.groupby('album_id').apply(
        #     lambda group: np.average(group['weighted_score'], weights=group['weight'])
        # ).reset_index(drop=True)
        #
        # # 更新 weighted_score，这里使用 .loc 明确修改
        # df.loc[df.index, 'new_weighted_score'] = new_weighted_scores
        # df.loc[df.index, 'weighted_score'] = df['new_weighted_score']

        # # 计算每个专辑的加权平均分数
        # df['new_weighted_score'] = df.groupby('album_id').apply(
        #     lambda group: np.average(group['weighted_score'], weights=group['weight'])
        # ).reindex(df['album_id']).reset_index(drop=True)
        #
        # # 更新加权评分
        # df['weighted_score'] = df['new_weighted_score']
        # 计算每个专辑的加权平均分数
        def compute_weighted_score(group):
            if group['weight'].sum() > 0:
                return np.average(group['weighted_score'], weights=group['weight'])
            else:
                return np.nan

        new_weighted_scores = df.groupby('album_id').apply(compute_weighted_score)
        new_weighted_scores = new_weighted_scores.reindex(df['album_id']).reset_index(drop=True)

        # 更新加权评分
        df['new_weighted_score'] = new_weighted_scores
        # df['weighted_score'] = df['new_weighted_score']
        df['weighted_score'] = df['new_weighted_score'].fillna(df['weighted_score'])

        print(df[['album_id', 'weighted_score']].drop_duplicates())

    return df


# 4. 执行迭代法计算
data_cleaned = iterative_weighting(data_cleaned, iterations=10)


# 5. 归一化到 10 分制
def normalize_to_10(df):
    df = df.copy()  # 创建副本，避免警告
    # # 将原始评分乘以 2
    # df['weighted_score'] *= 2
    # 为了增加得分的可变度，添加一个弹性系数
    scaling_factor = 1.5  # 根据需求进行调整

    # min_score = df['weighted_score'].min()
    # max_score = df['weighted_score'].max()
    # print(f"最小加权评分: {min_score}, 最大加权评分: {max_score}")  # 调试信息
    # if max_score == min_score:  # 避免除零
    #     df['final_score'] = 10  # 所有评分相同的情况下，设为最大值
    # else:
    #     # 将分数线性映射到 0-10
    #     df['final_score'] = 10 * (df['weighted_score'] - min_score) / (max_score - min_score)
    # 使用百分位数进行归一化
    min_weighted_score = df['weighted_score'].min()
    max_weighted_score = df['weighted_score'].max()

    print(f"最小加权评分: {min_weighted_score}, 最大加权评分: {max_weighted_score}")  # 调试信息

    df['final_score'] = (
            scaling_factor * (df['weighted_score'] - min_weighted_score) / (
                max_weighted_score - min_weighted_score) * 10
    )

    # 可选：防止最终分数超出范围
    df['final_score'] = df['final_score'].clip(0, 10)
    # # 使用 .loc 来避免 SettingWithCopyWarning
    # df.loc[:, 'final_score'] = 10 * (df['weighted_score'] - min_score) / (max_score - min_score)
    return df


data_cleaned = normalize_to_10(data_cleaned)

# 6. 按 album_id 分组，计算每个专辑的最终评分
final_album_scores = data_cleaned.groupby('album_id')['final_score'].mean().reset_index()

# 输出结果
print(final_album_scores)

# 保存为 CSV 文件
final_album_scores.to_csv('final_album_scores.csv', index=False)

# import pymysql
# from sqlalchemy import create_engine
# import pandas as pd
# import numpy as np
#
# # 使用 SQLAlchemy 连接数据库
# engine = create_engine("mysql+pymysql://root:root@localhost/bdt_database")
#
# # 从数据库中提取数据
# query = "SELECT * FROM rating;"
# data = pd.read_sql(query, engine)
#
# # 去除没有评分的评论
# data_cleaned = data.dropna(subset=['score']).copy()
# # 定义初始权重：根据 likes 和 length
# def calculate_initial_weight(row):
#     weight = row['likes']
#     if row['length'] == 1:  # 长评权重大
#         weight *= 1.5
#     return weight
#
# # 使用 .loc 明确指定要修改的列，确保修改的是原始数据
# data_cleaned.loc[:, 'weight'] = data_cleaned.apply(calculate_initial_weight, axis=1)
# def iterative_weighting(data_cleaned, iterations=10):
#     # 假设 'weighted_score' 列已经存在
#     if 'weighted_score' not in data_cleaned.columns:
#         # 创建 'weighted_score' 列，并初始化为 'score'
#         data_cleaned['weighted_score'] = data_cleaned['score']
#
#     # 创建 'new_weighted_score' 列，并初始化为 'weighted_score'
#     if 'new_weighted_score' not in data_cleaned.columns:
#         data_cleaned['new_weighted_score'] = data_cleaned['weighted_score']
#
#     for _ in range(iterations):
#         # 进行迭代计算
#         # 按 album_id 分组计算加权平均分数
#         new_weighted_scores = data_cleaned.groupby('album_id').apply(
#             lambda group: np.average(group['weighted_score'], weights=group['weight'])
#         ).reset_index(name='new_weighted_score')
#
#         # 更新 weighted_score，这里使用 .loc 明确修改
#         data_cleaned = data_cleaned.merge(new_weighted_scores, on='album_id', how='left')
#         data_cleaned.loc[data_cleaned.index, 'weighted_score'] = data_cleaned['new_weighted_score'].fillna(data_cleaned['weighted_score'])
#
#     return data_cleaned
# # 调用函数
# data_cleaned = iterative_weighting(data_cleaned, iterations=10)
# def normalize_to_10(df):
#     df = df.copy()  # 创建副本，避免警告
#
#     min_score = df['weighted_score'].min()
#     max_score = df['weighted_score'].max()
#
#     # 使用 .loc 来避免 SettingWithCopyWarning
#     df.loc[:, 'final_score'] = 10 * (df['weighted_score'] - min_score) / (max_score - min_score)
#     return df
#
# data_cleaned = normalize_to_10(data_cleaned)
# final_album_scores = data_cleaned.groupby('album_id')['final_score'].mean().reset_index()
#
# # 输出结果
# print(final_album_scores)
#
# # 可选：将结果保存为 CSV 文件
# final_album_scores.to_csv('final_album_scores.csv', index=False)
