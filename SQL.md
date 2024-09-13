# 数据库设置说明

## 简介
本项目的数据库用于存储音乐家和专辑的相关信息，以及用户对专辑的评分、点赞等内容。以下指南将帮助您在本地或服务器上搭建数据库。

## 环境要求
- MySQL 5.7 或以上版本
- MySQL 命令行工具或其他数据库管理工具（如 MySQL Workbench）

## 数据库表结构

### 1. `Album` 表

存储专辑的相关信息，包括专辑评分、评分计数、封面图片等。

```sql
CREATE TABLE Album
(
    id                INT AUTO_INCREMENT PRIMARY KEY,
    title             VARCHAR(255) NOT NULL,      -- 专辑标题
    rating            FLOAT,                      -- 用户评分（平均值）
    rating_count      INT,                        -- 评分人数
    cover_image       VARCHAR(255),               -- 专辑封面图片路径
    disc              TEXT,                       -- 唱片信息
    author            VARCHAR(100) NOT NULL,      -- 专辑作者（音乐家）
    seu_rating        FLOAT,                      -- 系统加权评分
    long_count        INT,                        -- 长评论计数
    short_count       INT,                        -- 短评论计数
    rating_difference FLOAT,                      -- 评分差异（用于算法计算）
    album_intro       TEXT                        -- 专辑简介
);
```

### 2. `Musician` 表

存储音乐家信息以及他们的前三张专辑。

```sql
CREATE TABLE Musician
(
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,           -- 音乐家姓名
    image_path   VARCHAR(255),                    -- 音乐家图片路径
    basic_info   TEXT,                            -- 基本信息
    introduction TEXT,                            -- 个人简介
    album1       INT,                             -- 音乐家第一张专辑ID
    album2       INT,                             -- 音乐家第二张专辑ID
    album3       INT                              -- 音乐家第三张专辑ID
);
```

### 3. `Musician_Album` 表

用于建立音乐家与专辑之间的多对多关联关系。

```sql
CREATE TABLE Musician_Album
(
    id          INT AUTO_INCREMENT PRIMARY KEY,
    musician_id INT,                              -- 音乐家ID（外键）
    album_id    INT,                              -- 专辑ID（外键）
    FOREIGN KEY (musician_id) REFERENCES Musician(id),
    FOREIGN KEY (album_id) REFERENCES Album(id)
);
```

### 4. `rating` 表

存储用户对专辑的评分及相关信息。

```sql
CREATE TABLE rating
(
    id      INT AUTO_INCREMENT PRIMARY KEY,
    album_id INT,                                 -- 专辑ID（外键）
    score   INT,                                  -- 用户评分
    likes   INT,                                  -- 点赞数
    length  TINYINT,                              -- 评分时长（区分长短评分）
    FOREIGN KEY (album_id) REFERENCES Album(id)
);
```

## 数据库搭建步骤

1. 确保MySQL服务已启动并可以访问。
2. 使用命令行或数据库管理工具连接到MySQL实例：
   ```bash
   mysql -u your_username -p
   ```
3. 创建新的数据库（例如：`music_db`）：
   ```sql
   CREATE DATABASE music_db;
   USE music_db;
   ```
4. 执行提供的SQL脚本来创建表：
   - 复制并粘贴上面提供的SQL语句到MySQL命令行工具或执行SQL文件。
   
5. 验证数据库表结构是否正确：
   ```sql
   SHOW TABLES;
   ```

## 维护和扩展
- 任何新增列或表的修改都需要与现有的业务逻辑保持一致。
- 如果需要更改外键关系，请确保处理相关联的数据，以防违反参照完整性。

---