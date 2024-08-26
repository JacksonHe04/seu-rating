import requests
import re
import os

# 起始目标
shouye_url = 'https://hifini.com/'
# 伪装
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

# 1.发请求，并且获得源码
def get_data(url):
    # 2.发请求
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_data = response.text  # 获得源码
        return html_data
    else:
        print(response.status_code)

# 2.解析要的数据
def parse_data(data):
    z = '<li\sclass="media\sthread\stap\s\s".*?>.*?<div\sclass="subject\sbr' \
        'eak-all">.*?<a\shref="(.*?)">(.*?)</a>'
    result = re.findall(z, data, re.S)
    # print(result)
    for i in result:
        # print(i)
        href = "https://hifini.com/" + i[0]  # 详情页链接  https://hifini.com/thread-28611.htm
        name = i[1]  # 歌名
        print(href)
        print(name)
        # https://hifini.com/get_music.php?key=fK+8XKMNFO7jUv5qJ7DYAn4u35SwmAGLa3vyR9fHKNUr9IFyZve8SjDiEWdbT8LDcmBdwakBtH3XJWmD758D
        print('=========')
        get_song_link(href)


# 3.向详情页发请求 获得网页源码
def get_song_link(link):  # link形参：模拟的是详情页URL
    # 调用请求函数（详情页的url）
    song_htm_data = get_data(link)
    # print("详情页的源码",song_htm_data)
    # 解析歌曲的播放资源
    song_re = "music:\s\[.*?title:\s'(.*?)',.*?url:\s'(.*?)',"
    r = re.findall(song_re, song_htm_data, re.S)
    print("歌曲信息：", r)
    for i in r:
        song_name = i[0]
        song_link = "https://hifini.com/" + i[1]
        print("歌名：", song_name)
        print("歌曲播放资源链接：", song_link)
        print('++++++++++')
        data_byts = requests.get(song_link, headers=headers).content
        # print(data_byts)

        if not os.path.exists('歌曲'):
            os.makedirs('歌曲')

        song_name = re.sub('[\/:*?"<>|]', '-', song_name)
        with open('歌曲\{}.m4a'.format(song_name), 'wb') as f:
            f.write(data_byts)

if __name__ == '__main__':
    h = get_data(shouye_url)
    # print(h)
    parse_data(h)