// // web/static/web002.js
// // 当DOM内容加载完成后，执行以下代码
// document.addEventListener('DOMContentLoaded', function () {
//     // 获取搜索表单元素
//     const form = document.getElementById('search-form');
//     // 获取结果显示区域元素
//     const resultsDiv = document.getElementById('results');
//
//     // 监听表单的提交事件
//     form.addEventListener('submit', async function (event) {
//         // 阻止表单的默认提交行为
//         event.preventDefault();
//
//         // 获取问题输入框元素
//         const questionInput = document.getElementById('question');
//         // 获取用户输入的艺术家名称
//         const artistName = questionInput.value;
//
//         try {
//             // 发送fetch请求
//             const response = await fetch(form.action || '/get_artist_info', {
//                 // 设置请求方法
//                 method: form.method,
//                 // 设置请求头
//                 headers: {
//                     'Content-Type': 'application/x-www-form-urlencoded',
//                 },
//                 // 设置请求体
//                 body: new URLSearchParams({ question: artistName })
//             });
//
//             // 如果响应状态不是200，抛出错误
//             if (!response.ok) {
//                 throw new Error(`HTTP error! Status: ${response.status}`);
//             }
//
//             // 解析响应数据为JSON
//             const data = await response.json();
//
//             // 清空结果显示区域
//             resultsDiv.innerHTML = '';
//             // 如果有错误信息，显示错误信息
//             if (data.error) {
//                 resultsDiv.innerHTML = `<p>${data.error}</p>`;
//             } else {
//                 // 构造结果显示HTML
//                 let output = '<ul>';
//                 for (const [key, value] of Object.entries(data)) {
//                     output += `<li><strong>${key}:</strong> ${value}</li>`;
//                 }
//                 output += '</ul>';
//                 // 显示结果
//                 resultsDiv.innerHTML = output;
//             }
//         } catch (error) {
//             // 如果发生错误，显示错误信息
//             resultsDiv.innerHTML = `<p>发生错误，请稍后再试。${error.message}</p>`;
//         }
//     });
// });
