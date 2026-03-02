# 🔥 全网热榜 - 实时新闻聚合

> 自动聚合知乎、微博、36 氪、虎嗅、IT 之家、掘金、GitHub 等平台热门新闻

**网站地址：** https://614153770.github.io/news-aggregator/

## ✨ 功能特点

- 🔄 **自动更新** - 每 5 分钟自动抓取最新热榜
- 📱 **多平台聚合** - 7+ 主流平台一站式查看
- 🎨 **美观界面** - 响应式设计，支持手机/电脑
- 📊 **分类浏览** - 按平台筛选，快速定位
- 📧 **订阅服务** - 日报/周报邮件订阅（即将上线）

## 📰 支持平台

| 平台 | 更新频率 | 状态 |
|------|----------|------|
| 知乎 | 每 5 分钟 | ✅ |
| 微博 | 每 5 分钟 | ✅ |
| 36 氪 | 每 5 分钟 | ✅ |
| 虎嗅 | 每 5 分钟 | ✅ |
| IT 之家 | 每 5 分钟 | ✅ |
| 掘金 | 每 5 分钟 | ✅ |
| GitHub | 每 5 分钟 | ✅ |

## 🚀 快速开始

### 查看网站

直接访问：https://614153770.github.io/news-aggregator/

### 本地运行

```bash
# 安装依赖
pip install requests beautifulsoup4

# 抓取新闻
cd scripts
python fetch_news.py

# 本地预览
cd ..
python -m http.server 8000
# 访问 http://localhost:8000
```

### 手动触发更新

1. 进入 GitHub Actions
2. 选择 "Auto Fetch News"
3. 点击 "Run workflow"

## 📁 项目结构

```
news-aggregator/
├── index.html              # 网站首页
├── data/                   # 新闻数据
│   ├── all_news.json       # 全部新闻
│   ├── zhihu_news.json     # 知乎
│   ├── weibo_news.json     # 微博
│   ├── 36kr_news.json      # 36 氪
│   ├── huxiu_news.json     # 虎嗅
│   ├── ithome_news.json    # IT 之家
│   ├── juejin_news.json    # 掘金
│   ├── github_news.json    # GitHub
│   └── news_summary.json   # 汇总报告
├── scripts/
│   └── fetch_news.py       # 抓取脚本
└── .github/workflows/
    └── auto-fetch.yml      # 定时任务
```

## 📧 订阅服务

**即将上线：**
- 📅 日报：每天早上 8 点推送前日 TOP20
- 📊 周报：每周日推送本周精选 + 趋势分析

**订阅方式：**
1. 访问 GitHub 仓库
2. 在 Issues 中留言订阅
3. 或发送邮件到 614153770@qq.com

## 🎯 后续计划

- [ ] 增加更多新闻源（豆瓣、少数派等）
- [ ] 用户注册/登录系统
- [ ] 在线订阅功能
- [ ] 搜索功能
- [ ] 热度趋势图表
- [ ] 移动端 APP

## ⚠️ 注意事项

- 所有数据来源于各平台公开 API
- 仅供学习交流使用
- 如有侵权请联系删除
- 商业使用请先联系作者

## 📄 License

MIT License

---

*由 AI 自动抓取并整理 | 数据每 5 分钟更新*
