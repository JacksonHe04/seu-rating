// document.getElementById('search-form').addEventListener('submit', function (event) {
//     event.preventDefault(); // 阻止表单默认提交行为
//
//     // 获取页面上id为artistName的元素的值，即艺术家的名字
//     const artistName = document.getElementById('question').value;
//
//
//     // 使用AJAX发送请求
//     const xhr = new XMLHttpRequest();
//     xhr.open('POST', '/get_artist_info', true);
//     <!-- 设置请求头的Content-Type为application/x-www-form-urlencoded，这表明发送给服务器的数据将是一个URL编码的字符串 -->
//     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//     xhr.onload = function () {
//         if (xhr.status === 200) {
//             // 处理返回的JSON数据
//             const result = JSON.parse(xhr.responseText);
//             displayResults(result);
//         } else {
//             console.error(xhr.statusText);
//         }
//     };
//     xhr.send('question=' + encodeURIComponent(artistName));
// });
//
// function displayResults(data) {
//     <!-- 获取搜索结果的div元素，用于后续操作 -->
//     const resultsDiv = document.getElementById('results');
//     // 根据data更新resultsDiv的内容
//     // 例如，如果data包含音乐类型，可以这样显示：
//     if (data['音乐类型']) {
//         resultsDiv.innerHTML += '<p>Music Type: ' + data['音乐类型'] + '</p>';
//     }
//     // 可以添加更多的逻辑来显示其他信息
// }
