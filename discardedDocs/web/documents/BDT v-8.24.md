# BDT v-8.24

## 项目简介

这是一个基于Web的音乐搜索系统，旨在帮助用户快速获取关于乐队的基本信息，如音乐类型和出道地点等。本项目使用了Flask作为后端框架，前端则采用了原生JavaScript实现。

## 技术栈

- **后端**: Python + Flask
- **前端**: HTML + CSS + JavaScript
- **爬虫**: Requests + BeautifulSoup

## 功能介绍

### 用户界面

- 用户可以通过输入乐队名称来查询乐队的相关信息。
- 查询结果将以列表的形式展示出来。

### 技术实现

1. **前端**:
   - 使用`DOMContentLoaded`事件确保DOM完全加载后执行脚本。
   - 表单提交时通过隐藏的iframe发送POST请求，避免页面刷新。
   - 使用JavaScript动态更新页面内容，提高用户体验。

2. **后端**:
   - Flask框架接收POST请求并处理。
   - 使用Requests库从Wikipedia抓取数据。
   - 使用BeautifulSoup解析HTML文档，提取所需信息。

3. **数据处理**:
   - 从Wikipedia获取乐队的音乐类型和出道地点。
   - 返回JSON格式的数据供前端展示。

## 安装与运行

1. **安装依赖**:
    ```bash 
    pip install flask flask-cors requests
    beautifulsoup4
2. **启动应用**:
    ```bash 
    python app.py
3. **访问应用**:
   - 访问终端给出的链接;
   - 如 `http://127.0.0.1:5000/` 即可看到应用首页。

## 注意事项

- 确保Python环境已安装好所有依赖包。
- 本项目仅用于学习交流，请勿用于商业用途。

## 贡献指南

- 如需贡献代码，请先创建一个新的分支进行开发。
- 完成开发后，提交PR至主分支。
- PR描述中请说明修改的内容及原因。

## 联系方式

- 作者: 何锦诚
- 邮箱: [JacksonHe04@outlook.com]
- QQ: [2466145536]

---

此README.md文件为项目成员何锦诚的仓库提供了详细的项目介绍和技术实现细节，便于其他成员理解和协作。


