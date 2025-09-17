# 热点资讯爬虫应用 - 逐步部署指南

## 🚀 第一步：准备GitHub仓库

### 1.1 创建GitHub账号（如果还没有）
- 访问 https://github.com
- 点击 "Sign up" 注册账号
- 完成邮箱验证

### 1.2 创建新仓库
1. 登录GitHub后，点击右上角 "+" → "New repository"
2. 填写仓库信息：
   - **Repository name**: `hotspot-crawler-app`
   - **Description**: `热点资讯爬虫应用 - 包含爬虫、数据库、API和前端`
   - 选择 **Public**（公开仓库）
   - ✅ 勾选 "Initialize this repository with a README"
   - 点击 **Create repository**

### 1.3 获取仓库URL
创建成功后，复制仓库的HTTPS URL，格式为：
`https://github.com/你的用户名/hotspot-crawler-app.git`

## 🖥️ 第二步：本地Git配置

### 2.1 打开命令提示符或PowerShell
按 `Win + R`，输入 `cmd` 或 `powershell`，按回车

### 2.2 进入项目目录
```bash
cd C:\Users\Administrator\CodeBuddy\20250917170115
```

### 2.3 初始化Git并推送代码
逐行执行以下命令：

```bash
# 初始化Git仓库
git init

# 添加所有文件到暂存区
git add .

# 提交更改
git commit -m "初始提交: 完整的爬虫应用系统"

# 添加GitHub远程仓库（替换为你的实际URL）
git remote add origin https://github.com/你的用户名/hotspot-crawler-app.git

# 重命名分支并推送到GitHub
git branch -M main
git --version

```

**注意**: 首次推送可能需要输入GitHub用户名和密码（建议使用Personal Access Token）

## ⚙️ 第三步：启用GitHub Pages

### 3.1 启用Pages功能
1. 在GitHub仓库页面，点击 **Settings** 标签
2. 左侧菜单选择 **Pages**
3. 在 "Build and deployment" → "Source" 选择 **GitHub Actions**
4. 系统会自动检测并配置Pages部署

### 3.2 等待首次部署完成
- 点击 **Actions** 标签查看部署进度
- 等待绿色的对勾出现，表示部署成功
- 访问你的GitHub Pages地址：`https://你的用户名.github.io/hotspot-crawler-app/`

## ⏰ 第四步：设置定时任务

### 4.1 启用Actions权限
1. 在仓库 **Settings** → **Actions** → **General**
2. 确保 "Allow all actions and reusable workflows" 被选中
3. 点击 **Save** 保存设置

### 4.2 检查定时任务配置
- 系统会自动检测 `.github/workflows/scheduled-crawler.yml` 文件
- 定时任务会在每30分钟自动执行

### 4.3 手动触发测试
1. 点击 **Actions** 标签
2. 选择 **Scheduled Data Crawling** 工作流
3. 点击 **Run workflow** → **Run workflow** 手动触发

## ☁️ 第五步：Cloudflare Pages部署

### 5.1 创建Cloudflare账号
1. 访问 https://dash.cloudflare.com/sign-up
2. 注册新账号或登录现有账号
3. 完成邮箱验证

### 5.2 连接GitHub仓库
1. 进入Cloudflare Dashboard
2. 选择 **Workers & Pages** → **Create application** → **Pages**
3. 点击 **Connect to Git**

### 5.3 配置部署设置
1. 选择你的GitHub账号，授权访问
2. 选择 `hotspot-crawler-app` 仓库
3. 点击 **Begin setup**

### 5.4 构建设置
- **Build command**: `echo "No build needed"`
- **Build output directory**: `.`
- **Python version**: `3.9`
- 点击 **Save and Deploy**

### 5.5 获取访问地址
- 部署完成后，Cloudflare会提供一个临时域名
- 格式如：`https://你的项目名.pages.dev`

## 🔧 第六步：验证部署

### 6.1 GitHub Pages验证
访问：`https://你的用户名.github.io/hotspot-crawler-app/`
- ✅ 页面应正常加载
- ✅ 导航功能正常工作
- ✅ 数据能够显示

### 6.2 Cloudflare Pages验证  
访问Cloudflare提供的域名
- ✅ 检查页面加载速度
- ✅ 测试所有功能模块

### 6.3 定时任务验证
1. 在GitHub仓库点击 **Actions**
2. 查看 **Scheduled Data Crawling** 的运行记录
3. 确认数据库文件 `hotspot_data.db` 有更新提交

## 📊 第七步：监控和维护

### 7.1 监控部署状态
- **GitHub Actions**: 查看工作流运行状态
- **Cloudflare Analytics**: 查看访问统计

### 7.2 错误处理
- 设置邮件通知：GitHub Settings → Notifications
- 定期检查日志文件

### 7.3 数据备份
- GitHub自动备份所有代码和历史
- 定期导出数据库备份

## 🆘 常见问题解决

### 问题1: Git推送失败
**解决方案**:
```bash
# 强制推送（谨慎使用）
git push -f origin main

# 或者先拉取再推送
git pull origin main --rebase
git push origin main
```

### 问题2: Actions权限错误
**解决方案**:
- 检查仓库Settings → Actions → General
- 确保工作流权限设置为允许

### 问题3: Cloudflare部署失败
**解决方案**:
- 检查构建设置是否正确
- 确保所有必要文件都已提交

### 问题4: 定时任务不执行
**解决方案**:
- 检查cron语法：`*/30 * * * *`
- 确认仓库的Actions功能已启用

## 📞 支持资源

- **GitHub文档**: https://docs.github.com
- **Cloudflare文档**: https://developers.cloudflare.com/pages
- **问题反馈**: 在Git仓库提交Issue

---

**部署完成时间**: 2025-09-17  
**状态**: 所有部署文件准备就绪，等待执行