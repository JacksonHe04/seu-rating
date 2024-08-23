# web/app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__, static_folder='static', template_folder='templates')  # 设置静态文件夹和模板文件夹
CORS(app)

# 在根目录下提供服务
@app.route('/')
def serve_index():
    # send_from_directory函数用于发送指定目录下的文件
    # 将应用的静态资源目录下的web001.html和web001.css文件返回给客户端
    return send_from_directory(app.static_folder, 'web001.html')

# 定义路由和请求方法，处理通过POST请求访问'/get_band_info'路径的请求
@app.route('/get_band_info', methods=['POST'])
def get_band_info():
    # 从请求的表单数据中获取乐队名称
    band_name = request.form.get('question')
    # band_name = request.form.get('band_name')

    # 构建查询乐队信息的URL
    # 使用乐队名称替换空格为下划线，以符合Wikipedia页面的命名规范
    url = f"https://zh.wikipedia.org/wiki/{band_name.replace(' ', '_')}"

    # 发送HTTP GET请求
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析HTML文档
        # 使用BeautifulSoup解析响应文本，以便于提取有用的数据
        soup = BeautifulSoup(response.text, 'html.parser')

        # 初始化结果字典
        result = {}

        # 查找音乐类型
        # 通过查找特定的表格标题来识别和获取音乐类型的信息
        music_type = soup.find('th', string='音乐类型')
        # 如果找到音乐类型信息
        if music_type:
            # 寻找下一个兄弟<td>元素，以获取详细的音乐类型内容
            music_type = music_type.find_next_sibling('td')
            # 如果找到了音乐类型的内容
            if music_type:
                # 将音乐类型的文字内容添加到结果字典中，strip=True用于去除空格
                result['音乐类型'] = music_type.get_text(strip=True)

        # 查找出道地点
        debut_location = soup.find('th', string='出道地点')
        if debut_location:
            debut_location = debut_location.find_next_sibling('td')
            if debut_location:
                result['出道地点'] = debut_location.get_text(strip=True)

        return jsonify(result)
    else:
        return jsonify({'error': '无法获取页面'}), 404

# 运行下面这行代码启动Flask应用，然后打开终端给出的链接即可进入搜索项目网页
if __name__ == '__main__':
    app.run(debug=True)
