# BDTrueValueRecSys README

## 项目简介
我们是东南大学22级的人工智能专业本科生蒋妙、何锦诚、吴锦承。
BDTrueValueRecSys 是2024年暑期学校《专业技能实训》课程中的项目。该项目旨在开发一个基于大数据的真实值推荐系统，利用先进的算法和技术为用户提供音乐推荐服务。

## 软件架构
我们的软件架构包括前端和后端两个主要部分：
- **前端**：采用 HTML、CSS 和 JavaScript 构建用户界面，实现交互功能。
- **后端**：使用 Python 开发业务逻辑（爬虫和算法）。
- **框架**：使用 Django 框架开发项目，并实现前后的联调。
- **数据库**：使用 MySQL 作为数据库管理系统，存储用户评论数据、推荐结果等。

## 安装教程

1. 确保您的计算机上安装了 Python 3 和 MySQL。
2. 克隆本仓库到本地：
   ```bash
   git clone https://gitee.com/your_username/BDTrueValueRecSys.git
   ```
3. 进入项目目录并安装所需的 Python 库：
   ```bash
   cd BDTrueValueRecSys
   pip install
   ```
4. 配置 MySQL 数据库，并导入数据库脚本（详情见 spider 和 rec 文件夹中的说明）。

## 使用说明

1. 启动 MySQL 服务并确保数据库已正确配置。
2. 在 djangoProjectPro 目录下，运行 python manage.py runserver 启动项目网页。
3. 使用浏览器访问前端页面，通常为 `http://localhost:8000` （根据实际配置可能有所不同）。
4. 根据界面提示输入相关信息，即可开始使用推荐系统。

## 参与贡献

1. Fork 本仓库。
2. 新建 `Feat_xxx` 分支。
3. 提交代码。
4. 新建 Pull Request。
5. 
## 开发说明
#### 在 PyCharm 安装 Gitee 插件
1. 设置
2. 插件
3. 搜索 Gitee
4. 安装并重启 PyCharm

#### 在终端生成 SSH 公钥
https://help.gitee.com/repository/ssh-key/generate-and-add-ssh-public-key

#### 添加 Gitee 的 SSH 公钥
https://blog.csdn.net/Mian_Rainy/article/details/137188006?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_utm_term~default-0-137188006-blog-121550649.235^v43^pc_blog_bottom_relevance_base1&spm=1001.2101.3001.4242.1&utm_relevant_index=1

#### 管理者：把 Pycharm 上的代码通过 Git 上传到 Gitee
1. 创建本地仓库
2. 共享到 Gitee 仓库

#### 管理者：邀请开发者加入仓库
https://blog.csdn.net/qq_22841387/article/details/120734861

#### 开发者：将仓库克隆到 PyCharm 本地并关联
1. VCS
2. 从版本控制中获取
3. 输入 URL

#### 开发者：在本地编写代码文件并上传
1. 编写好代码
2. Git
3. 提交
4. 编写描述
5. 推送
6. 到 Gitee 仓库检查

#### 管理者：审核

开源开发者提交 PR 的流程
https://help.gitee.com/base/pullrequest/Fork+Pull

## 请忽视以下文件或目录：
1. .venv
2. discardedDocs
3. node_modules
4. package.json
5. packsge-lock.json
---
感谢您阅读我们的项目文档，期待您的反馈和建议！