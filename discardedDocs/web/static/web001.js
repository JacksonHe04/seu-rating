// // web/static/web001.js
// // 当DOM内容加载完成后，执行以下代码
// // 什么是DOM内容？
// // 回答：网页文档对象模型（DOM）是网页内容的结构化表示形式，它定义了网页中各种元素的结构、属性和关系。
// // DOM 是网页内容的抽象表示，通过编程语言（如 JavaScript）可以操作和修改网页内容。
// // 为指定的DOM元素添加事件监听器
// document.addEventListener
//
// // 当文档结构加载完毕后，执行匿名函数
// ('DOMContentLoaded', function () {
//     // 获取搜索表单元素，用于后续的表单提交事件处理
//     const form = document.getElementById('search-form');
//     // 获取用于展示结果的div元素
//     const resultsDiv = document.getElementById('results');
//     // 获取隐藏的iframe，用于在后台进行搜索请求，避免页面跳转
//     const hiddenIframe = document.getElementById('hidden-iframe');
//
//     // 当表单提交事件被触发时，捕获事件并执行以下函数
//     form.addEventListener('submit', function (event) {
//         // 阻止表单的默认提交行为，以防止页面刷新
//         event.preventDefault();
//
//         // 获取问题输入框的DOM元素，用于后续操作
//         const questionInput = document.getElementById('question');
//         // 读取输入框中的值，这通常用于获取用户输入的乐队名称
//         const bandName = questionInput.value;
//
//         // 将表单数据发送到隐藏的 iframe 中
//         const formData = new FormData();
//         formData.append('band_name', bandName);
//         // 设置隐藏iframe的srcdoc属性，以程序化的方式构建一个表单
//         hiddenIframe.srcdoc = `
//             <form action="${form.action}" method="${form.method}" target="hidden-iframe">
//                 <input type="hidden" name="band_name" value="${bandName}">
//                 <input type="submit" value="Submit">
//             </form>
//         `;
//         // 提交隐藏的iframe中的表单
//         // 此操作触发forms数组中索引为0的表单提交事件
//         hiddenIframe.contentWindow.document.forms[0].submit();
//
//         // 处理 iframe 中的响应
//         hiddenIframe.onload = function () {
//             // 获取隐藏iframe的内容文档，以便于后续提取其中的数据
//             const iframeDoc = hiddenIframe.contentDocument || hiddenIframe.contentWindow.document;
//
//             // 提取iframe中body标签的文本内容，并去除首尾空白字符，用于后续处理或展示
//             const responseText = iframeDoc.body.textContent.trim();
//
//             // 检查响应文本是否为JSON格式
//             if (responseText.startsWith('{')) {
//                 // 解析JSON文本
//                 const data = JSON.parse(responseText);
//                 // 清空结果显示区域
//                 resultsDiv.innerHTML = '';
//                 // 检查数据中是否包含错误信息
//                 if (data.error) {
//                     // 如果有错误，显示错误信息
//                     resultsDiv.innerHTML = `<p>${data.error}</p>`;
//                 } else {
//                     // 否则，遍历数据并构建显示列表
//                     let output = '<ul>';
//                     for (const [key, value] of Object.entries(data)) {
//                         // 动态生成列表项
//                         output += `<li><strong>${key}:</strong> ${value}</li>`;
//                     }
//                     // 关闭列表标签
//                     output += '</ul>';
//                     // 更新结果显示区域
//                     resultsDiv.innerHTML = output;
//                 }
//             } else {
//                 // 如果响应文本格式不正确，显示通用错误消息
//                 resultsDiv.innerHTML = `<p>发生错误，请稍后再试。</p>`;
//             }
//         }
//     })
// })