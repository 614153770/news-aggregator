#!/usr/bin/env python3
"""
全网热榜聚合抓取脚本 v2
修复乱码问题，增加更多新闻源
支持：知乎、微博、36 氪、虎嗅、IT 之家、掘金、GitHub、豆瓣、少数派、澎湃新闻等
"""

import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re
import html

class NewsFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def decode_content(self, content):
        """智能解码内容，修复乱码"""
        if isinstance(content, bytes):
            # 尝试多种编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'big5', 'latin-1']
            for encoding in encodings:
                try:
                    return content.decode(encoding)
                except:
                    continue
            return content.decode('utf-8', errors='ignore')
        return content
    
    def clean_text(self, text):
        """清理文本，去除多余空格和 HTML 实体"""
        if not text:
            return ''
        text = html.unescape(text)  # 转换 HTML 实体
        text = re.sub(r'\s+', ' ', text)  # 多个空格变一个
        text = text.strip()
        return text
    
    def fetch_zhihu(self):
        """抓取知乎热榜 - 使用免登录接口"""
        print("📌 抓取知乎热榜...")
        try:
            # 使用第三方镜像或免登录接口
            url = "https://api.zhihu.com/topstory/hot-lists/total?limit=20&reverse_order=0"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 401:
                # 如果仍需登录，使用备用方案
                return self._fetch_zhihu_backup()
            
            data = response.json()
            items = []
            
            for item in data.get('data', [])[:20]:
                target = item.get('target', {})
                title = self.clean_text(target.get('title', ''))
                if title:
                    items.append({
                        'title': title,
                        'url': f"https://www.zhihu.com/question/{target.get('id', '')}",
                        'source': '知乎',
                        'hot': f"🔥 {target.get('answer_count', 0)} 回答",
                        'platform': 'zhihu'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ⚠️ 知乎主接口失败，使用备用：{e}")
            return self._fetch_zhihu_backup()
    
    def _fetch_zhihu_backup(self):
        """知乎备用抓取方案"""
        try:
            url = "https://www.zhihu.com/hot"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            items = []
            
            # 查找热榜项目
            for item in soup.find_all('div', class_='HotItem', limit=20):
                title_elem = item.find('h2', class_='HotItem-title')
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    link = title_elem.find('a')
                    url = link.get('href', '') if link else ''
                    if title and url:
                        items.append({
                            'title': title,
                            'url': f"https://www.zhihu.com{url}" if url.startswith('/') else url,
                            'source': '知乎',
                            'hot': '🔥 热榜',
                            'platform': 'zhihu'
                        })
            
            print(f"  ✅ 知乎备用抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ❌ 知乎备用也失败：{e}")
            return []
    
    def fetch_weibo(self):
        """抓取微博热搜 - 使用移动端接口"""
        print("📌 抓取微博热搜...")
        try:
            url = "https://m.weibo.cn/api/container/getIndex?containerid=102803"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            items = []
            cards = data.get('data', {}).get('cards', [])
            
            if cards:
                card_group = cards[0].get('card_group', []) if len(cards) > 0 else []
                for item in card_group[:20]:
                    desc = self.clean_text(item.get('desc', ''))
                    if desc and len(desc) > 2:
                        items.append({
                            'title': desc,
                            'url': f"https://s.weibo.com/weibo?q={desc.replace(' ', '%20')}",
                            'source': '微博',
                            'hot': '🔥 热搜',
                            'platform': 'weibo'
                        })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ⚠️ 微博抓取失败：{e}")
            return self._mock_weibo()
    
    def _mock_weibo(self):
        """微博模拟数据"""
        return [
            {'title': '微博热搜数据获取中', 'url': 'https://s.weibo.com/', 'source': '微博', 'hot': '⏳', 'platform': 'weibo'},
        ]
    
    def fetch_36kr(self):
        """抓取 36 氪"""
        print("📌 抓取 36 氪...")
        try:
            url = "https://36kr.com/"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            
            items = []
            # 查找文章链接
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                title = self.clean_text(link.get_text())
                
                if '/p/' in href and len(title) > 5 and len(title) < 100:
                    items.append({
                        'title': title,
                        'url': f"https://36kr.com{href}" if href.startswith('/p/') else href,
                        'source': '36 氪',
                        'hot': '💼 科技',
                        'platform': '36kr'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:15]
        except Exception as e:
            print(f"  ❌ 36 氪抓取失败：{e}")
            return []
    
    def fetch_huxiu(self):
        """抓取虎嗅"""
        print("📌 抓取虎嗅...")
        try:
            url = "https://www.huxiu.com/"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            
            items = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                title = self.clean_text(link.get_text())
                
                if '/article/' in href and len(title) > 5 and len(title) < 100:
                    items.append({
                        'title': title,
                        'url': f"https://www.huxiu.com{href}" if href.startswith('/article/') else href,
                        'source': '虎嗅',
                        'hot': '💡 观点',
                        'platform': 'huxiu'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:15]
        except Exception as e:
            print(f"  ❌ 虎嗅抓取失败：{e}")
            return []
    
    def fetch_ithome(self):
        """抓取 IT 之家"""
        print("📌 抓取 IT 之家...")
        try:
            url = "https://www.ithome.com/"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            
            items = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                title = self.clean_text(link.get_text())
                
                if 'html' in href and len(title) > 8 and len(title) < 100:
                    full_url = href if href.startswith('http') else f"https://www.ithome.com{href}"
                    items.append({
                        'title': title,
                        'url': full_url,
                        'source': 'IT 之家',
                        'hot': '💻 科技',
                        'platform': 'ithome'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:20]
        except Exception as e:
            print(f"  ❌ IT 之家抓取失败：{e}")
            return []
    
    def fetch_juejin(self):
        """抓取掘金"""
        print("📌 抓取掘金...")
        try:
            url = "https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            items = []
            for item in data.get('data', [])[:20]:
                article = item.get('article_info', {})
                title = self.clean_text(article.get('title', ''))
                if title:
                    items.append({
                        'title': title,
                        'url': f"https://juejin.cn/post/{article.get('article_id', '')}",
                        'source': '掘金',
                        'hot': f"👍 {item.get('article_info', {}).get('digg_count', 0)}",
                        'platform': 'juejin'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ❌ 掘金抓取失败：{e}")
            return []
    
    def fetch_github(self):
        """抓取 GitHub Trending"""
        print("📌 抓取 GitHub Trending...")
        try:
            url = "https://github.com/trending"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            
            items = []
            articles = soup.find_all('article', class_='Box-row')[:15]
            
            for article in articles:
                name_elem = article.find('h2', class_='h3').find('a')
                if name_elem:
                    name = self.clean_text(name_elem.get_text())
                    url = 'https://github.com' + name_elem['href']
                    desc_elem = article.find('p', class_='col-9')
                    desc = self.clean_text(desc_elem.get_text()) if desc_elem else ''
                    
                    items.append({
                        'title': f"{name}" + (f" - {desc[:40]}..." if desc else ""),
                        'url': url,
                        'source': 'GitHub',
                        'hot': '⭐ Trending',
                        'platform': 'github'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ❌ GitHub 抓取失败：{e}")
            return []
    
    def fetch_douban(self):
        """抓取豆瓣"""
        print("📌 抓取豆瓣...")
        try:
            url = "https://www.douban.com/"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            
            items = []
            # 查找豆瓣热点
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                title = self.clean_text(link.get_text())
                
                if 'douban.com/note/' in href or 'movie.douban.com' in href:
                    if len(title) > 5 and len(title) < 100:
                        items.append({
                            'title': title,
                            'url': href,
                            'source': '豆瓣',
                            'hot': '🎬 娱乐',
                            'platform': 'douban'
                        })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:15]
        except Exception as e:
            print(f"  ❌ 豆瓣抓取失败：{e}")
            return []
    
    def fetch_sspai(self):
        """抓取少数派"""
        print("📌 抓取少数派...")
        try:
            url = "https://sspai.com/"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            
            items = []
            for link in soup.find_all('a', href=True, class_=lambda x: x and 'title' in str(x).lower()):
                href = link.get('href', '')
                title = self.clean_text(link.get_text())
                
                if href.startswith('/post/') and len(title) > 5:
                    items.append({
                        'title': title,
                        'url': f"https://sspai.com{href}",
                        'source': '少数派',
                        'hot': '📱 数码',
                        'platform': 'sspai'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:15]
        except Exception as e:
            print(f"  ❌ 少数派抓取失败：{e}")
            return []
    
    def fetch_thepaper(self):
        """抓取澎湃新闻"""
        print("📌 抓取澎湃新闻...")
        try:
            url = "https://www.thepaper.cn/"
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(self.decode_content(response.content), 'html.parser')
            
            items = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                title = self.clean_text(link.get_text())
                
                if 'detail' in href and len(title) > 8 and len(title) < 100:
                    items.append({
                        'title': title,
                        'url': href if href.startswith('http') else f"https://www.thepaper.cn{href}",
                        'source': '澎湃新闻',
                        'hot': '📰 新闻',
                        'platform': 'thepaper'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:15]
        except Exception as e:
            print(f"  ❌ 澎湃新闻抓取失败：{e}")
            return []
    
    def fetch_all(self):
        """抓取所有源"""
        print(f"\n{'='*60}")
        print(f"🚀 开始抓取全网热榜 v2 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        all_items = []
        
        # 依次抓取各平台
        all_items.extend(self.fetch_zhihu())
        all_items.extend(self.fetch_weibo())
        all_items.extend(self.fetch_36kr())
        all_items.extend(self.fetch_huxiu())
        all_items.extend(self.fetch_ithome())
        all_items.extend(self.fetch_juejin())
        all_items.extend(self.fetch_github())
        all_items.extend(self.fetch_douban())
        all_items.extend(self.fetch_sspai())
        all_items.extend(self.fetch_thepaper())
        
        # 添加时间戳
        timestamp = datetime.now().isoformat()
        for item in all_items:
            item['fetched_at'] = timestamp
        
        print(f"\n{'='*60}")
        print(f"✅ 抓取完成！共 {len(all_items)} 条新闻")
        
        # 统计各平台数量
        platform_count = {}
        for item in all_items:
            platform = item['platform']
            platform_count[platform] = platform_count.get(platform, 0) + 1
        
        for platform, count in platform_count.items():
            print(f"  {platform}: {count} 条")
        
        print(f"{'='*60}\n")
        
        return all_items

def save_to_json(data, filepath):
    """保存数据到 JSON"""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 数据已保存到 {filepath}")

def main():
    fetcher = NewsFetcher()
    items = fetcher.fetch_all()
    
    if items:
        # 保存完整数据
        save_to_json(items, 'data/all_news.json')
        
        # 保存分类数据
        platforms = {}
        for item in items:
            platform = item['platform']
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(item)
        
        for platform, platform_items in platforms.items():
            save_to_json(platform_items, f'data/{platform}_news.json')
        
        # 生成汇总报告
        report = {
            'update_time': datetime.now().isoformat(),
            'total_count': len(items),
            'platforms': {k: len(v) for k, v in platforms.items()},
            'top_10': items[:10]
        }
        save_to_json(report, 'data/news_summary.json')
        
        print("\n✨ 所有数据已保存完成！")
    else:
        print("\n❌ 未抓取到任何数据")

if __name__ == "__main__":
    main()
