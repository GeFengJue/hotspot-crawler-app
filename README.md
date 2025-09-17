# 热点资讯爬虫应用

一个完整的网络热点资讯爬虫系统，包含数据抓取、数据库存储、RESTful API和响应式前端界面。

## 功能特性

- 🔍 **多源数据抓取**：支持同花顺、雪球、东方财富等多个数据源
- 💾 **SQLite数据库**：本地数据存储和管理
- 🚀 **Flask API**：RESTful接口提供数据服务
- 📱 **响应式前端**：适配手机和电脑的现代化界面
- ⏰ **定时任务**：自动定时抓取数据
- 🔧 **易于部署**：支持GitHub Pages和Cloudflare Pages

## 项目结构

```
hotspot-crawler-app/
├── complete_hotspot_crawler.py  # 主爬虫程序
├── api_server.py               # Flask API服务器
├── static_server.py           # 静态文件服务器
├── database_manager.py        # 数据库管理
├── scheduled_crawler.py       # 定时任务脚本
├── index.html                # 前端界面
├── hotspot_data.db           # SQLite数据库
├── requirements.txt          # Python依赖
├── deploy-config.json        # 部署配置
└── README.md                 # 说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

**启动API服务器：**
```bash
python api_server.py
```

**启动静态文件服务器：**
```bash
python static_server.py
```

**执行数据抓取：**
```bash
python complete_hotspot_crawler.py
```

### 3. 访问应用

打开浏览器访问：`http://localhost:8000`

## API接口

### 获取热点资讯
```
GET /api/hot_news
```

### 获取今日热点
```
GET /api/today_hotspot
```

### 获取公社热帖
```
GET /api/hot_news?type=公社热帖
```

### 获取财经日历
```
GET /api/financial_calendar
```

## 定时任务

配置每30分钟自动执行数据抓取：

```bash
python scheduled_crawler.py
```

## 部署指南

### GitHub Pages部署

1. 创建GitHub仓库
2. 推送代码到main分支
3. 启用GitHub Pages，选择gh-pages分支

### Cloudflare Pages部署

1. 连接GitHub仓库到Cloudflare Pages
2. 配置构建设置：
   - 构建命令: `python -m py_compile *.py`
   - 构建输出目录: `.`
   - Python版本: 3.11

### 本地部署

```bash
# 启动所有服务
python api_server.py & python static_server.py
```

## 技术栈

- **后端**: Python 3.8+, Flask, SQLite
- **前端**: HTML5, CSS3, JavaScript, jQuery, Bootstrap
- **爬虫**: Requests, BeautifulSoup4, lxml
- **部署**: GitHub Pages, Cloudflare Pages

## 配置说明

### 数据库配置
数据库文件: `hotspot_data.db`
表结构: 自动创建和管理

### 服务器配置
- API服务器端口: 5000
- 静态服务器端口: 8000
- CORS已启用，支持跨域访问

## 开发指南

### 添加新的数据源

1. 在 `complete_hotspot_crawler.py` 中添加新的爬虫方法
2. 在 `api_server.py` 中添加对应的API路由
3. 在前端 `index.html` 中添加导航按钮和渲染逻辑

### 自定义样式

修改 `index.html` 中的CSS样式部分，支持响应式设计：
- 手机端: <768px
- 平板端: 769px-1024px
- 桌面端: >1024px

## 故障排除

### 常见问题

1. **端口冲突**: 修改 `static_server.py` 和 `api_server.py` 中的端口号
2. **依赖安装失败**: 确保使用Python 3.8+版本
3. **数据抓取失败**: 检查网络连接和目标网站可用性

### 日志查看

查看控制台输出获取详细错误信息。

## 许可证

MIT License - 详见 LICENSE 文件

## 支持

如有问题请提交Issue或联系开发团队。

---

**注意**: 请遵守目标网站的robots.txt协议，合理使用爬虫功能。