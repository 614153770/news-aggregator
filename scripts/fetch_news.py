#!/usr/bin/env python3
"""
全网热榜聚合抓取脚本
支持：知乎、微博、36 氪、虎嗅、IT 之家、掘金、GitHub 等
"""

import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import re

class NewsFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        self.results = []
    
    def fetch_zhihu(self):
        """抓取知乎热榜"""
        print("📌 抓取知乎热榜...")
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20&reverse_order=0"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            items = []
            for item in data.get('data', []):
                target = item.get('target', {})
                items.append({
                    'title': target.get('title', ''),
                    'url': f"https://www.zhihu.com/question/{target.get('id', '')}",
                    'source': '知乎',
                    'hot': target.get('bound_topic_entries', [{}])[0].get('bound_topic', {}).get('introduction', '') or f"{target.get('answer_count', 0)} 个回答",
                    'platform': 'zhihu'
                })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ❌ 知乎抓取失败：{e}")
            return []
    
    def fetch_weibo(self):
        """抓取微博热搜"""
        print("📌 抓取微博热搜...")
        try:
            # 使用移动端 API
            url = "https://m.weibo.cn/api/container/getIndex?containerid=102803_ctg1_4188_-_ctg1_4188_domain&_status=0"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            items = []
            cards = data.get('data', {}).get('cards', [])
            if cards and len(cards) > 0:
                card_group = cards[0].get('card_group', [])
                for item in card_group[:20]:
                    items.append({
                        'title': item.get('desc', ''),
                        'url': f"https://s.weibo.com/weibo?q={item.get('desc', '').replace(' ', '%20')}",
                        'source': '微博',
                        'hot': item.get('pic', '') or '热搜',
                        'platform': 'weibo'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ❌ 微博抓取失败：{e}")
            # 返回模拟数据
            return self._mock_weibo()
    
    def _mock_weibo(self):
        """微博抓取失败时返回模拟数据"""
        return [
            {'title': '模拟微博热搜 1', 'url': 'https://s.weibo.com/', 'source': '微博', 'hot': '模拟', 'platform': 'weibo'},
            {'title': '模拟微博热搜 2', 'url': 'https://s.weibo.com/', 'source': '微博', 'hot': '模拟', 'platform': 'weibo'},
        ]
    
    def fetch_36kr(self):
        """抓取 36 氪"""
        print("📌 抓取 36 氪...")
        try:
            url = "https://36kr.com/"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = []
            
            # 查找文章链接
            for link in soup.find_all('a', href=True)[:15]:
                href = link['href']
                title = link.get_text(strip=True)
                if href.startswith('/p/') and len(title) > 10:
                    items.append({
                        'title': title,
                        'url': f"https://36kr.com{href}",
                        'source': '36 氪',
                        'hot': '热门',
                        'platform': '36kr'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:10]
        except Exception as e:
            print(f"  ❌ 36 氪抓取失败：{e}")
            return []
    
    def fetch_huxiu(self):
        """抓取虎嗅"""
        print("📌 抓取虎嗅...")
        try:
            url = "https://www.huxiu.com/"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = []
            
            for link in soup.find_all('a', href=True, class_=lambda x: x and 'article' in str(x).lower())[:15]:
                href = link.get('href', '')
                title = link.get_text(strip=True)
                if href.startswith('/article/') and len(title) > 5:
                    items.append({
                        'title': title,
                        'url': f"https://www.huxiu.com{href}",
                        'source': '虎嗅',
                        'hot': '热门',
                        'platform': 'huxiu'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:10]
        except Exception as e:
            print(f"  ❌ 虎嗅抓取失败：{e}")
            return []
    
    def fetch_ithome(self):
        """抓取 IT 之家"""
        print("📌 抓取 IT 之家...")
        try:
            url = "https://www.ithome.com/"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = []
            
            # 查找新闻列表
            for link in soup.find_all('a', href=True):
                href = link['href']
                title = link.get_text(strip=True)
                if 'html' in href and len(title) > 10 and len(title) < 100:
                    if not href.startswith('http'):
                        href = f"https://www.ithome.com{href}"
                    items.append({
                        'title': title,
                        'url': href,
                        'source': 'IT 之家',
                        'hot': '热门',
                        'platform': 'ithome'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items[:10]
        except Exception as e:
            print(f"  ❌ IT 之家抓取失败：{e}")
            return []
    
    def fetch_juejin(self):
        """抓取掘金"""
        print("📌 抓取掘金...")
        try:
            url = "https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            items = []
            for item in data.get('data', [])[:15]:
                article = item.get('article_info', {})
                items.append({
                    'title': article.get('title', ''),
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
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = []
            
            articles = soup.find_all('article', class_='Box-row')[:10]
            for article in articles:
                name_elem = article.find('h2', class_='h3').find('a')
                if name_elem:
                    name = name_elem.get_text(strip=True)
                    url = 'https://github.com' + name_elem['href']
                    desc_elem = article.find('p', class_='col-9')
                    desc = desc_elem.get_text(strip=True) if desc_elem else ''
                    
                    items.append({
                        'title': f"{name} - {desc[:50]}..." if desc else name,
                        'url': url,
                        'source': 'GitHub',
                        'hot': 'Trending',
                        'platform': 'github'
                    })
            
            print(f"  ✅ 抓取 {len(items)} 条")
            return items
        except Exception as e:
            print(f"  ❌ GitHub 抓取失败：{e}")
            return []
    
    def fetch_all(self):
        """抓取所有源"""
        print(f"\n{'='*50}")
        print(f"🚀 开始抓取全网热榜 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}\n")
        
        all_items = []
        
        # 依次抓取各平台
        all_items.extend(self.fetch_zhihu())
        all_items.extend(self.fetch_weibo())
        all_items.extend(self.fetch_36kr())
        all_items.extend(self.fetch_huxiu())
        all_items.extend(self.fetch_ithome())
        all_items.extend(self.fetch_juejin())
        all_items.extend(self.fetch_github())
        
        # 添加时间戳
        timestamp = datetime.now().isoformat()
        for item in all_items:
            item['fetched_at'] = timestamp
        
        print(f"\n{'='*50}")
        print(f"✅ 抓取完成！共 {len(all_items)} 条新闻")
        print(f"{'='*50}\n")
        
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
