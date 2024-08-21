document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault(); // 阻止表单默认提交

    const query = document.getElementById("question").value;
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "正在搜索，请稍候...";

    // 使用搜索引擎API进行搜索（例如Google Custom Search API）
    const apiKey = 'YOUR_API_KEY'; // 你需要在API提供者那申请一个API key
    const searchEngineId = 'YOUR_SEARCH_ENGINE_ID';
    const url = `https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${searchEngineId}&q=${encodeURIComponent(query)}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.items && data.items.length > 0) {
                resultsDiv.innerHTML = '';
                data.items.forEach(item => {
                    const resultItem = document.createElement("div");
                    resultItem.innerHTML = `<a href="${item.link}" target="_blank">${item.title}</a><p>${item.snippet}</p>`;
                    resultsDiv.appendChild(resultItem);
                });
            } else {
                resultsDiv.innerHTML = "未找到相关结果。";
            }
        })
        .catch(error => {
            resultsDiv.innerHTML = "搜索出错，请稍后再试。";
            console.error("搜索错误:", error);
        });
});