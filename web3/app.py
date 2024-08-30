# web/app.py
import os

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from flask import render_template

app = Flask(__name__, static_folder='static', template_folder='templates')  # 设置静态文件夹和模板文件夹
CORS(app)

# web/app.py
# 导入必要的库和模块
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from flask import render_template

# 创建Flask应用实例，设置静态文件夹和模板文件夹
app = Flask(__name__, static_folder='static', template_folder='templates')
# 配置跨域资源共享（CORS），允许所有来源的请求
CORS(app)

# 在根目录下提供服务
@app.route('/')
def serve_index():
    # send_from_directory函数用于发送指定目录下的文件
    # 将应用的静态资源目录下的web301.html返回给客户端
    return app.send_static_file('index.html')

# 定义路由和请求方法，处理获取艺术家信息的请求
@app.route('/get_artist_info', methods=['POST'])
def get_artist_info():
    # 从请求的表单数据中获取名称
    artist_name = request.form.get('question')
    # 构建查询艺术家信息的URL
    url = f"https://zh.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"
    # 发送HTTP GET请求
    response = requests.get(url)
    # 检查响应状态码
    if response.status_code == 200:
        # 解析HTML文档
        soup = BeautifulSoup(response.text, 'lxml')
        # 初始化结果字典
        result = {}
        # 查找h1标题
        h1_title = soup.find('h1', class_='firstHeading')
        if h1_title:
            h1_title = h1_title.find('span')
            result['艺术家名称'] = h1_title.get_text(strip=True)
        # 查找音乐类型
        music_type = soup.find('th', string='音乐类型')
        if music_type:
            music_type = music_type.find_next_sibling('td')
            if music_type:
                result['音乐类型'] = music_type.get_text(strip=True)
        # 查找出道地点
        debut_location = soup.find('th', string='出道地点')
        if debut_location:
            debut_location = debut_location.find_next_sibling('td')
            if debut_location:
                result['出道地点'] = debut_location.get_text(strip=True)
        # 查找活跃年代
        active_years = soup.find('th', string='活跃年代')
        if active_years:
            active_years = active_years.find_next_sibling('td')
            if active_years:
                result['活跃年代'] = active_years.get_text(strip=True)
        # 查找唱片公司
        record_label = soup.find('th', string='唱片公司')
        if record_label:
            record_label = record_label.find_next_sibling('td')
            if record_label:
                result['唱片公司'] = record_label.get_text(strip=True)
        # 查找网站
        website = soup.find('th', string='网站')
        if website:
            website = website.find_next_sibling('td')
            if website:
                result['网站'] = website.get_text(strip=True)
    # 将结果数据转换为JSON格式并返回
    return jsonify(result)

# 当脚本是作为主程序运行时，启动Flask应用服务器
if __name__ == '__main__':
    app.run(debug=True)

# 在根目录下提供服务
@app.route('/')
def serve_index():
    # send_from_directory函数用于发送指定目录下的文件
    # 将应用的静态资源目录下的web301.html返回给客户端
    return app.send_static_file('index.html')


@app.route('/get_artist_info', methods=['POST'])
# 上面这句话的'/get_artist_info'是什么意思？
# 回答：'/get_artist_info'是应用中定义的路由，用于处理通过POST请求访问'/get_artist_info'路径的请求。
# 回答：POST是一种HTTP请求方法，用于向服务器发送数据，通常用于提交表单数据。
def get_artist_info():
    # 从请求的表单数据中获取名称
    artist_name = request.form.get('question')

    # 构建查询艺术家信息的URL
    url = f"https://zh.wikipedia.org/wiki/{artist_name.replace(' ', '_')}"

    # 发送HTTP GET请求
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析HTML文档
        soup = BeautifulSoup(response.text, 'lxml')

        # 初始化结果字典
        result = {}

        # 查找h1标题
        h1_title = soup.find('h1', class_='firstHeading')
        if h1_title:
            h1_title = h1_title.find('span')
            result['艺术家名称'] = h1_title.get_text(strip=True)

        # 查找音乐类型
        music_type = soup.find('th', string='音乐类型')
        if music_type:
            music_type = music_type.find_next_sibling('td')
            if music_type:
                result['音乐类型'] = music_type.get_text(strip=True)

        # 查找出道地点
        debut_location = soup.find('th', string='出道地点')
        if debut_location:
            debut_location = debut_location.find_next_sibling('td')
            if debut_location:
                result['出道地点'] = debut_location.get_text(strip=True)

        # 查找活跃年代
        active_years = soup.find('th', string='活跃年代')
        if active_years:
            active_years = active_years.find_next_sibling('td')
            if active_years:
                result['活跃年代'] = active_years.get_text(strip=True)

        # 查找唱片公司
        record_label = soup.find('th', string='唱片公司')
        if record_label:
            record_label = record_label.find_next_sibling('td')
            if record_label:
                result['唱片公司'] = record_label.get_text(strip=True)

        # 查找网站
        website = soup.find('th', string='网站')
        if website:
            website = website.find_next_sibling('td')
            if website:
                result['网站'] = website.get_text(strip=True)

    # 将结果数据转换为JSON格式并返回
    return jsonify(result)
    # 在这段代码中，jsonify 是 Flask 框架提供的一个函数，用于将 Python 字典转换为 JSON 格式的响应，并设置正确的 MIME 类型为 application/json。这使得客户端能够正确地解析响应内容。
    # jsonify 函数:
    # 作用: 将 Python 字典或列表转换为 JSON 格式的字符串，并自动设置 HTTP 响应头部的 Content-Type 为 application/json。
    # 返回值: 返回一个 Flask Response 对象，其内容是 JSON 格式的字符串。
    # 含义: result 是一个字典，其中包含了从 Wikipedia 页面解析得到的艺术家信息，例如音乐类型和出道地点等。
    # 示例: {'音乐类型': '流行音乐', '出道地点': '纽约'}
    # jsonify(result):
    # 将 result 字典转换为 JSON 格式的字符串。
    # 设置 HTTP 响应头部的 Content-Type 为 application/json。
    # 返回一个 Flask Response 对象，其内容是 JSON 格式的字符串。
    # return jsonify(result):
    # 作用: 将处理后的 JSON 数据作为 HTTP 响应返回给客户端。
    # 效果: 客户端接收到的响应将是一个 JSON 格式的字符串，客户端可以通过 JavaScript 等方式解析这个字符串，并在网页上显示相关信息。
    # 示例输出:
    # 假设 result 的值为 {'音乐类型': '流行音乐', '出道地点': '纽约'}，那么 jsonify(result) 的输出将是这样的 JSON 字符串：

# 脚本是作为主程序运行
if __name__ == '__main__':
    app.run(debug=True)
