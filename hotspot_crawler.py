import requests
import json
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime

class HotSpotCrawler:
    def __init__(self):
        self.base_url = "https://duanxianxia.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/web/hotnews/web'
        })
    
    def get_hot_news(self, news_type):
        """获取不同类型的热点新闻"""
        url = f"{self.base_url}/api/getHotNewsByType"
        
        payload = {
            'type': news_type
        }
        
        try:
            response = self.session.post(url, data=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('result') == 'success':
                return self.parse_hot_news(data.get('html', ''), news_type)
            else:
                return f"获取{news_type}数据失败: {data}"
                
        except Exception as e:
            return f"请求错误: {str(e)}"
    
    def parse_hot_news(self, html_content, news_type):
        """解析HTML内容，提取热点信息"""
        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('div', class_='item flex')
        
        results = []
        
        for item in items:
            try:
                # 提取排名
                no_div = item.find('div', class_='no')
                rank = no_div.get_text(strip=True) if no_div else "无排名"
                
                # 提取标题和链接
                title_link = item.find('a')
                if title_link:
                    title = title_link.get_text(strip=True)
                    href = title_link.get('href', '')
                    # 确保链接完整
                    if href and not href.startswith('http'):
                        href = f"https:{href}" if href.startswith('//') else href
                else:
                    title = "无标题"
                    href = ""
                
                # 提取时间
                time_span = item.find('span', class_='time')
                publish_time = time_span.get_text(strip=True) if time_span else "未知时间"
                
                # 提取热度
                heat_span = item.find('span', string=re.compile(r'热度：\d+'))
                heat = heat_span.get_text(strip=True).replace('热度：', '') if heat_span else "0"
                
                result = {
                    'rank': rank,
                    'title': title,
                    'link': href,
                    'publish_time': publish_time,
                    'heat': heat,
                    'type': news_type
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"解析项目时出错: {e}")
                continue
        
        return results
    
    def get_all_hotspots(self):
        """获取所有类型的热点内容"""
        hotspot_types = {
            'ths': '热点资讯',
            'chaosha': '今日热点', 
            'jiuyan': '公社热帖',
            'timeline': '财经日历'
        }
        
        all_results = {}
        
        for type_key, type_name in hotspot_types.items():
            print(f"正在获取{type_name}...")
            results = self.get_hot_news(type_key)
            all_results[type_name] = results
            time.sleep(1)  # 避免请求过于频繁
        
        return all_results
    
    def save_to_file(self, data, filename=None):
        """保存数据到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hotspot_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """主函数"""
    print("开始抓取热点聚焦数据...")
    
    crawler = HotSpotCrawler()
    
    # 获取所有热点数据
    all_data = crawler.get_all_hotspots()
    
    # 打印结果
    for category, items in all_data.items():
        print(f"\n=== {category} ===")
        for i, item in enumerate(items[:5], 1):  # 只显示前5条
            print(f"{i}. {item['title']} (热度: {item['heat']})")
            if item['link']:
                print(f"   链接: {item['link']}")
    
    # 保存到文件
    filename = crawler.save_to_file(all_data)
    print(f"\n数据已保存到: {filename}")

if __name__ == "__main__":
    main()