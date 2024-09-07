import axios from "axios";

// 设置后端 API 的基础 URL
const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000/api",  // Django 服务器的 API 端点
    headers: {
        "Content-Type": "application/json",
    },
});

export default {
    // 获取音乐人列表
    getMusicians() {
        return apiClient.get("/musicians/");
    },
};