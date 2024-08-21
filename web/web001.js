// 获取搜索表单元素，为其添加提交事件监听器
document.getElementById("search-form").addEventListener("submit", function(event) {
    // 阻止表单默认提交行为，以便用JavaScript处理搜索请求
    event.preventDefault();

    // 获取用户输入的查询内容
    const query = document.getElementById("question").value;
    // 获取展示结果的容器
    const resultsDiv = document.getElementById("results");
    // 设置初始搜索状态提示
    resultsDiv.innerHTML = "正在搜索，请稍候...";

    // 构建搜索引擎API请求URL，此处使用Google Custom Search API作为示例
    const apiKey = 'YOUR_API_KEY'; // 你需要在API提供者那申请一个API key
    const searchEngineId = 'YOUR_SEARCH_ENGINE_ID'; // 每个Google自定义搜索引擎都有一个唯一的ID
    // 根据用户查询内容构建完整的API请求URL
    const url = `https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${searchEngineId}&q=${encodeURIComponent(query)}`;

    // 发送API请求，获取搜索结果
    fetch(url)
        .then(response => response.json()) // 解析API返回的JSON数据
        .then(data => {
            // 检查搜索结果中是否有相关项
            if (data.items && data.items.length > 0) {
                // 清空结果容器，准备展示新的搜索结果
                resultsDiv.innerHTML = '';
                // 遍历搜索结果项，创建并添加展示元素到结果容器
                data.items.forEach(item => {
                    const resultItem = document.createElement("div");
                    // 构建每个搜索结果的标题和摘要
                    resultItem.innerHTML = `<a href="${item.link}" target="_blank">${item.title}</a><p>${item.snippet}</p>`;
                    resultsDiv.appendChild(resultItem);
                });
            } else {
                // 如果没有找到相关结果，提示用户
                resultsDiv.innerHTML = "未找到相关结果。";
            }
        })
        .catch(error => {
            // 如果搜索过程中出现错误，提示用户，并在控制台记录错误详情
            resultsDiv.innerHTML = "搜索出错乐！请稍后再试。";
            console.error("搜索错误:", error);
        });
});
