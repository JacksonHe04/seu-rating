document.querySelector('.artist_bt').addEventListener('keyup', function(event) {
    // 检查是否按下了回车键
    if (event.key === 'Enter') {
        var artistName = this.value;
        // 执行搜索逻辑
        performSearch(artistName);
    }
});

// 获取搜索按钮并为其添加点击事件
document.querySelector('.search_bt').addEventListener('click', function() {
    var input = document.querySelector('.artist_bt');
    // 执行搜索逻辑
    performSearch(input.value);
});

function performSearch(artistName) {
    // 发送请求到后端
    fetch('/search', {
        // 指定HTTP请求的方法为POST，用于向服务器提交数据
        method: 'POST',
        // 设置请求头信息，告知服务器请求体的内容类型为JSON
        headers: {'Content-Type': 'application/json'},
        // 将艺术家的名字封装成JSON格式的字符串作为请求体的内容
        // 这里的artistName是准备发送给服务器的艺术家名字
        body: JSON.stringify({ artist: artistName })
    })
    .then(response => response.json())
    .then(data => {
        // 处理后端返回的数据
        console.log(data);
        // 这里可以更新页面显示结果
        navigateToArtistPage(data.artist);
    })
    .catch(error => {
        console.error('pffJs/search.js的performSearch函数发生错误啦', error);
    });
}

function navigateToArtistPage(artistName) {
    // 跳转到新页面
    window.location.href = '/get_artist?artist=' + encodeURIComponent(artistName);
}