#!/usr/bin/env python3
"""
新闻聚合站上线通知
"""

import requests
from datetime import datetime

SENDKEY = "SCT317686TjoxF0q9tBMkRPd6AvhWR5v1G"

def send_wechat(title, content):
    url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    params = {"title": title, "desp": content}
    try:
        response = requests.get(url, params=params, timeout=15)
        return response.json()
    except Exception as e:
        return {"code": -1, "error": str(e)}

def main():
    content = f"""
🎉 **全网热榜聚合站上线成功！**

━━━━━━━━━━━━━━━━

🌐 **网站信息**

**网站地址：** 
https://614153770.github.io/news-aggregator/

**GitHub 仓库：** 
https://github.com/614153770/news-aggregator

━━━━━━━━━━━━━━━━

📰 **已支持平台（7 个）**

✅ IT 之家 - 26 条
✅ 掘金 - 15 条  
✅ GitHub - 10 条
⏳ 知乎 - 需登录（优化中）
⏳ 微博 - 需登录（优化中）
⏳ 36 氪 - 优化中
⏳ 虎嗅 - 优化中

**首次抓取：** 51 条新闻

━━━━━━━━━━━━━━━━

🔄 **更新频率**

- **自动更新：** 每 5 分钟
- **GitHub Actions：** 自动执行
- **手动触发：** 可随时运行

━━━━━━━━━━━━━━━━

📧 **订阅服务**

**即将上线：**
- 📅 日报：每天 8:00 推送
- 📊 周报：每周日推送

**当前订阅方式：**
GitHub Issues 留言或邮件订阅

━━━━━━━━━━━━━━━━

🎯 **后续优化**

1. 修复知乎/微博登录问题
2. 增加更多新闻源
3. 用户注册/登录系统
4. 在线订阅功能
5. 搜索和筛选

━━━━━━━━━━━━━━━━

💡 **两个项目同时进行**

1. **AI Tech Daily** 
   https://614153770.github.io/auto-tech-content/
   - 每日 GitHub Trending + AI 分析

2. **全网热榜**
   https://614153770.github.io/news-aggregator/
   - 多平台新闻聚合

━━━━━━━━━━━━━━━━

✅ 小明同学 | AI 助手
"""
    
    result = send_wechat("🎉 全网热榜聚合站上线！", content)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if result.get("code") == 0:
        print(f"[{timestamp}] 通知发送成功")
    else:
        print(f"[{timestamp}] 通知发送失败：{result}")

if __name__ == "__main__":
    main()
