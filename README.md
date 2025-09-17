# hotspot-crawler-app
`热点资讯爬虫应用 - 包含爬虫、数据库、API和前端`

## 🚀 功能特性

- **多源数据爬取**: 支持同花顺、公社、财联社等多个数据源
- **实时数据更新**: 每30分钟自动抓取最新热点资讯
- **RESTful API**: 提供完整的数据接口服务
- **响应式前端**: 支持桌面和移动端访问
- **自动化部署**: 支持GitHub Pages和Cloudflare Pages部署

## 📦 部署配置

### GitHub Actions 自动化

项目包含两个GitHub Actions工作流：

1. **定时爬虫任务** (`scheduled-crawler.yml`)
   - 每30分钟自动执行数据抓取
   - 自动提交数据库更新

2. **自动部署** (`deploy.yml`)
   - 推送代码时自动部署到GitHub Pages
   - 支持手动触发部署

### 部署步骤

1. **推送到GitHub仓库**
   ```bash
   git add .
   git commit -m "初始化项目"
   git branch -M main
   git remote add origin https://github.com/your-username/hotspot-crawler-app.git
   git push -u origin main
   ```

2. **启用GitHub Pages**
   - 访问仓库的Settings → Pages
   - 选择Source为"GitHub Actions"
   - 保存设置

3. **配置Cloudflare Pages** (可选)
   - 连接GitHub仓库到Cloudflare Pages
   - 构建命令: `python -m py_compile *.py`
   - 输出目录: `.`

## 🔧 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动API服务器
python api_server.py

# 启动静态文件服务器  
python static_server.py

# 执行数据爬取
python complete_hotspot_crawler.py
```

## 📊 API接口

- `GET /api/hotspots` - 获取所有热点数据
- `GET /api/hotspots/today` - 获取今日热点
- `GET /api/hotspots/date/2024-01-01` - 按日期获取热点
- `GET /api/sources` - 获取数据源列表

## 🌐 在线访问

部署完成后可通过以下地址访问：
- GitHub Pages: `https://your-username.github.io/hotspot-crawler-app/`
- Cloudflare Pages: `https://your-project.pages.dev/`

## 📝 许可证

MIT License
