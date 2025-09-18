# 热点聚焦数据抓取系统

这是一个用于抓取和展示热点资讯、今日热点、公社热帖、财经日历等内容的完整系统。

## 功能特性

- 🔥 **热点资讯**：实时抓取热点新闻资讯
- 📈 **今日热点**：展示当日热门话题
- 💬 **公社热帖**：社区热门讨论帖子
- 📅 **财经日历**：重要财经事件日历
- 🌐 **RESTful API**：提供完整的数据接口
- 📱 **响应式前端**：适配各种设备的界面

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动API服务器
```bash
python api_server.py
```

### 3. 启动静态文件服务器
```bash
python static_server.py
```

### 4. 访问前端
打开浏览器访问：http://localhost:8081/index.html

## API接口

### 获取热点资讯
```
GET /api/hot_news
参数：limit (可选，默认50)
```

### 获取今日热点
```
GET /api/today_hotspot
参数：limit (可选，默认20)
```

### 获取公社热帖
```
GET /api/community_posts
参数：limit (可选，默认50)
```

### 获取财经日历
```
GET /api/financial_calendar
参数：limit (可选，默认50), date (可选，日期过滤)
```

### 获取数据统计
```
GET /api/statistics
```

## GitHub Actions 自动部署

系统配置了GitHub Actions，每天自动运行5次抓取任务：
- 北京时间 9:00
- 北京时间 12:00  
- 北京时间 15:00
- 北京时间 18:00
- 北京时间 21:00

## 项目结构

```
├── api_server.py          # Flask API服务器
├── database_manager.py    # 数据库管理
├── fix_crawler.py         # 数据抓取修复工具
├── hotspot_data.db        # SQLite数据库
├── index.html             # 前端页面
├── static_server.py       # 静态文件服务器
├── .github/workflows/     # GitHub Actions配置
│   └── hotspot-crawler.yml
└── README.md              # 项目说明
```

## 部署说明

1. 将项目上传到GitHub仓库
2. 启用GitHub Pages（用于前端部署）
3. GitHub Actions会自动运行定时抓取任务
4. 数据会自动提交到仓库

## 故障排除

如果遇到数据加载失败：
1. 检查API服务器是否运行：`http://127.0.0.1:5000/api/hot_news`
2. 检查静态服务器是否运行：`http://localhost:8081`
3. 确保数据库文件存在且可访问

## 技术支持

如有问题，请检查：
- API服务器日志
- 浏览器开发者工具控制台
- GitHub Actions运行状态