# BDTrueValueRecSys

#### 介绍
我们是东南大学22级的人工智能专业本科生蒋妙、何锦诚、吴锦承。
BDTrueValueRecSys 是2024年暑期学校《专业技能实训》课程中的项目。该项目旨在开发一个基于大数据的真实值推荐系统，利用先进的算法和技术为用户提供精准的推荐服务。

#### 软件架构
我们的软件架构包括前端和后端两个主要部分：
- **前端**：采用 HTML、CSS 和 JavaScript 构建用户界面，实现交互功能。
- **后端**：使用 Python 开发业务逻辑，MySQL 作为数据库管理系统，负责数据存储和检索。

#### 安装教程

1. 确保您的计算机上安装了 Python 3 和 MySQL。
2. 克隆本仓库到本地：
   ```bash
   git clone https://gitee.com/your_username/BDTrueValueRecSys.git
   ```
3. 进入项目目录并安装所需的 Python 库：
   ```bash
   cd BDTrueValueRecSys
   pip install -r requirements.txt
   ```
4. 配置 MySQL 数据库，并导入数据库脚本（详情见数据库文件夹中的说明）。

#### 使用说明

1. 启动 MySQL 服务并确保数据库已正确配置。
2. 在项目根目录下，运行后端服务：
   ```bash
   python app.py
   ```
3. 使用浏览器访问前端页面，通常为 `http://localhost:5000` （根据实际配置可能有所不同）。
4. 根据界面提示输入相关信息，即可开始使用推荐系统。

#### 参与贡献

1. Fork 本仓库。
2. 新建 `Feat_xxx` 分支。
3. 提交代码。
4. 新建 Pull Request。

---
感谢您阅读我们的项目文档，期待您的反馈和建议！