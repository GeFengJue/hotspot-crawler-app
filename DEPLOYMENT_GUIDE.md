# 热点资讯爬虫应用 - 详细部署指南

## 第一步：GitHub 仓库创建和代码推送

### 1. 创建GitHub仓库
1. 登录GitHub账号
2. 点击右上角"+" → "New repository"
3. 填写仓库信息：
   - Repository name: `hotspot-crawler-app`
   - Description: `热点资讯爬虫应用 - 包含爬虫、数据库、API和前端`
   - 选择 Public（公开）
   - 勾选 "Initialize this repository with a README"
   - 点击 "Create repository"

### 2. 本地Git初始化
```bash
# 进入项目目录
cd C:\Users\Administrator\CodeBuddy\20250917170115

# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 提交更改
git commit -m "初始提交: 完整的爬虫应用系统"

# 添加GitHub远程仓库
git remote add origin https://github.com/你的用户名/hotspot-crawler-app.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

## 第二步：GitHub Pages 部署

### 1. 启用GitHub Pages
1. 在GitHub仓库页面，点击 "Settings"
2. 左侧菜单选择 "Pages"
3. 在 "Build and deployment" → "Source" 选择 "GitHub Actions"
4. 系统会自动检测并配置Pages部署

### 2. 创建GitHub Actions工作流
在项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: pip install -r requirements.txt
      
    - name: Build static files
      run: |
        mkdir -p dist
        cp index.html dist/
        cp -r functions/ dist/functions/ || true
        cp _redirects dist/ || true
        
    - name: Setup Pages
      uses: actions/configure-pages@v4
      
    - name: Upload artifact
      uses: actions/upload-pages-artifact@v4
      with:
        path: 'dist'
        
    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v4
```

## 第三步：配置定时任务（GitHub Actions）

### 1. 创建定时爬虫工作流
创建 `.github/workflows/scheduled-crawler.yml`：

```yaml
name: Scheduled Data Crawling

on:
  schedule:
    - cron: '*/30 * * * *'  # 每30分钟执行一次
  workflow_dispatch:

jobs:
  crawl:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # 获取完整历史记录用于提交
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: pip install -r requirements.txt
      
    - name: Run crawler
      run: python complete_hotspot_crawler.py
      
    - name: Check for database changes
      id: check-changes
      run: |
        if git diff --quiet hotspot_data.db; then
          echo "changes=false" >> $GITHUB_OUTPUT
        else
          echo "changes=true" >> $GITHUB_OUTPUT
        fi
        
    - name: Commit and push database updates
      if: steps.check-changes.outputs.changes == 'true'
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        git add hotspot_data.db
        git commit -m "Auto-update database $(date +'%Y-%m-%d %H:%M:%S')"
        git push
        
    - name: No changes notification
      if: steps.check-changes.outputs.changes == 'false'
      run: echo "No database changes detected"
```

## 第四步：Cloudflare Pages 部署

### 1. 准备Cloudflare部署
1. 登录Cloudflare账号
2. 进入 "Workers & Pages" → "Create application" → "Pages"
3. 选择 "Connect to Git"

### 2. 连接GitHub仓库
1. 选择你的GitHub账号
2. 选择 `hotspot-crawler-app` 仓库
3. 点击 "Begin setup"

### 3. 配置构建设置
- **Build command**: `echo "No build needed for Python app"`
- **Build output directory**: `.`
- **Python version**: `3.9`

### 4. 环境变量配置（如果需要）
在Cloudflare Pages设置中添加环境变量：
- `PYTHON_VERSION`: `3.9`
- `FLASK_ENV`: `production`

### 5. 自定义域名（可选）
1. 在Cloudflare Pages设置中选择 "Custom domains"
2. 添加你的自定义域名
3. 按照提示配置DNS记录

## 第五步：验证部署

### GitHub Pages 验证
1. 访问: `https://你的用户名.github.io/hotspot-crawler-app/`
2. 检查页面是否能正常加载
3. 查看GitHub Actions运行状态

### Cloudflare Pages 验证  
1. 访问Cloudflare提供的默认域名
2. 检查应用功能是否正常
3. 测试API接口访问

## 第六步：监控和维护

### 1. 监控定时任务
- 定期检查GitHub Actions运行日志
- 监控数据库更新情况

### 2. 错误处理
- 设置邮件通知用于Action失败提醒
- 定期检查应用日志

### 3. 数据备份
- 定期导出数据库备份
- 使用Git历史记录追踪数据变化

## 故障排除

### 常见问题

1. **GitHub Actions 失败**
   - 检查Python版本兼容性
   - 验证依赖安装是否正确

2. **Cloudflare 部署问题**
   - 检查构建配置
   - 验证静态文件路径

3. **定时任务不执行**
   - 检查cron语法
   - 查看Action运行权限

## 安全注意事项

1. **API密钥保护**: 不要将敏感信息提交到GitHub
2. **访问控制**: 配置合适的CORS策略
3. **数据隐私**: 确保爬取数据符合网站使用条款

## 性能优化建议

1. **CDN加速**: 利用Cloudflare的全球CDN
2. **缓存策略**: 配置合适的缓存头
3. **数据库优化**: 定期清理历史数据

---

**部署完成时间**: 2025-09-17  
**状态**: 部署指南准备就绪