# Cloudflare Pages 部署指南

## 问题描述
GitHub Pages 数据已更新，但 Cloudflare Pages 数据未同步更新。

## 解决方案
已创建 Cloudflare Pages 专用部署工作流 (`.github/workflows/deploy-cloudflare.yml`)，需要配置以下密钥：

## 需要配置的 GitHub Secrets

### 1. CLOUDFLARE_API_TOKEN
- 获取方式：登录 Cloudflare Dashboard → 个人资料 → API Tokens → 创建Token
- 权限：需要包含 Pages 编辑权限
- 建议权限：`Account -> Cloudflare Pages -> Edit`

### 2. CLOUDFLARE_ACCOUNT_ID
- 获取方式：登录 Cloudflare Dashboard → Overview → 右侧栏找到 Account ID
- 格式：32位字符，如 `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p`

## 配置步骤

### 步骤 1：在 GitHub 仓库设置 Secrets
1. 进入您的 GitHub 仓库
2. 点击 Settings → Secrets and variables → Actions
3. 点击 New repository secret
4. 添加以下两个secret：
   - Name: `CLOUDFLARE_API_TOKEN`
   - Value: 您的Cloudflare API Token
   
   - Name: `CLOUDFLARE_ACCOUNT_ID` 
   - Value: 您的Cloudflare Account ID

### 步骤 2：确认 Cloudflare Pages 项目名称
在 `.github/workflows/deploy-cloudflare.yml` 中确认项目名称：
```yaml
projectName: hotspot-crawler-app  # 确保这与您的Cloudflare Pages项目名称一致
```

### 步骤 3：手动触发首次部署
1. 在 GitHub 仓库的 Actions 标签页
2. 找到 "Deploy to Cloudflare Pages" 工作流
3. 点击 "Run workflow" 手动触发部署

## 自动部署机制
配置完成后，以下情况会自动触发 Cloudflare Pages 部署：
1. 推送到 main 分支（当 index.html 或数据文件变化时）
2. 定时爬虫任务完成后
3. 手动触发工作流

## 缓存说明
Cloudflare CDN 缓存可能导致数据更新延迟，通常需要 1-5 分钟刷新缓存。

## 验证部署
部署完成后，访问您的 Cloudflare Pages URL 检查数据是否更新。