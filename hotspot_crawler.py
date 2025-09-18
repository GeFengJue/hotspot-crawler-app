import requests
import json
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime
import random
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hotspot_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class HotSpotCrawler:
    def __init__(self):
        self.base_url = "https://duanxianxia.com"
        self.backup_urls = [
            "https://ddxia.pages.dev",
            "https://hot.duanxianxia.com"
        ]
        self.session = self.create_session()
        self.current_url_index = 0
    
    def create_session(self):
        """创建带有重试机制的会话"""
        session = requests.Session()
        
        # 设置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # 设置请求头
        session.headers.update(self.get_headers())
        
        # 禁用系统代理，避免在GitHub Actions环境中出现问题
        session.trust_env = False
        
        return session
    
    def get_headers(self):
        """获取随机的浏览器头信息"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/web/hotnews/web',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        }
    
    def rotate_url(self):
        """轮换URL地址"""
        self.current_url_index = (self.current_url_index + 1) % len(self.backup_urls)
        return self.backup_urls[self.current_url_index]
    
    def get_hot_news(self, news_type, max_retries=3):
        """获取不同类型的热点新闻，支持重试和URL轮换"""
        for attempt in range(max_retries):
            try:
                current_base_url = self.backup_urls[self.current_url_index] if attempt > 0 else self.base_url
                url = f"{current_base_url}/api/getHotNewsByType"
                
                payload = {
                    'type': news_type
                }
                
                # 每次请求更新headers
                self.session.headers.update(self.get_headers())
                
                logging.info(f"尝试获取 {news_type} 数据 (尝试 {attempt + 1}/{max_retries})")
                response = self.session.post(url, data=payload, timeout=15)
                response.raise_for_status()
                
                data = response.json()
                if data.get('result') == 'success':
                    html_content = data.get('html', '')
                    if html_content:
                        results = self.parse_hot_news(html_content, news_type)
                        logging.info(f"成功获取 {news_type} {len(results)} 条数据")
                        return results
                    else:
                        logging.warning(f"{news_type} 返回空HTML内容")
                else:
                    logging.warning(f"{news_type} API返回失败: {data}")
                
                # 如果失败，轮换URL
                if attempt < max_retries - 1:
                    self.rotate_url()
                    logging.info(f"轮换到备用URL: {self.backup_urls[self.current_url_index]}")
                    time.sleep(2)  # 等待一段时间再重试
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"第 {attempt + 1} 次尝试获取 {news_type} 失败: {str(e)}")
                if attempt < max_retries - 1:
                    self.rotate_url()
                    logging.info(f"请求异常，轮换到备用URL: {self.backup_urls[self.current_url_index]}")
                    time.sleep(3)
                else:
                    logging.error(f"获取 {news_type} 数据全部尝试失败")
            except Exception as e:
                logging.error(f"处理 {news_type} 数据时发生未知错误: {str(e)}")
                break
        
        return []
    
    def parse_hot_news(self, html_content, news_type):
        """解析HTML内容，提取热点信息"""
        if not html_content or html_content.strip() == '':
            logging.warning("HTML内容为空，无法解析")
            return []
            
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 处理不同类型的HTML结构
            if news_type in ['ths', 'jiuyan']:
                # 热点资讯和公社热帖
                return self._parse_regular_hotspot(soup, news_type)
            elif news_type == 'chaosha':
                # 今日热点
                return self._parse_today_hotspot(soup)
            elif news_type == 'timeline':
                # 财经日历
                return self._parse_financial_calendar(html_content)
            else:
                return []
                
        except Exception as e:
            logging.error(f"解析HTML内容失败: {e}")
            return []
    
    def _parse_regular_hotspot(self, soup, news_type):
        """解析常规热点资讯"""
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
                    'type': '热点资讯' if news_type == 'ths' else '公社热帖',
                    'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                results.append(result)
                
            except Exception as e:
                logging.error(f"解析项目时出错: {e}")
                continue
        
        return results
    
    def _parse_today_hotspot(self, soup):
        """解析今日热点"""
        results = []
        
        try:
            # 查找所有panel-danger面板（每个面板代表一个日期）
            panels = soup.find_all('div', class_='panel panel-danger')
            
            if not panels:
                logging.warning("未找到今日热点面板")
                return []
            
            for panel in panels:
                # 解析日期标题
                date_div = panel.find('div', class_='panel-heading')
                date_text = date_div.get_text(strip=True) if date_div else ""
                
                # 查找面板主体
                panel_body = panel.find('div', class_='panel-body')
                if not panel_body:
                    continue
                
                # 查找所有关键词块
                keyword_blocks = panel_body.find_all('div', class_='keyword')
                
                for keyword_block in keyword_blocks:
                    # 提取标题
                    title_b = keyword_block.find('b')
                    title = title_b.get_text(strip=True) if title_b else keyword_block.get_text(strip=True)
                    
                    # 查找对应的关键词和热度信息（下一个兄弟元素）
                    next_sibling = keyword_block.find_next_sibling('div', style="color:#999;")
                    if next_sibling:
                        # 提取关键词
                        keyword_i = next_sibling.find('i')
                        keyword = keyword_i.get_text(strip=True) if keyword_i else ""
                        
                        # 提取热度值
                        heat_span = next_sibling.find('span')
                        heat = heat_span.get_text(strip=True).replace('热度值：', '') if heat_span else ""
                    else:
                        keyword = ""
                        heat = ""
                    
                    result = {
                        'rank': "",  # 今日热点没有排名
                        'title': title,
                        'link': "",  # 今日热点没有链接
                        'publish_time': date_text,
                        'heat': heat,
                        'type': '今日热点',
                        'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    results.append(result)
                
        except Exception as e:
            logging.error(f"解析今日热点失败: {e}")
        
        return results
    
    def _parse_financial_calendar(self, html_content):
        """解析财经日历"""
        results = []
        
        try:
            # 将HTML内容转换为BeautifulSoup对象
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 解析所有panel元素（每个panel代表一个日期）
            panels = soup.find_all('div', class_='panel panel-danger')
            
            for panel in panels:
                # 提取日期标题
                date_heading = panel.find('div', class_='panel-heading')
                date_text = date_heading.get_text(strip=True) if date_heading else ""
                
                # 提取该日期下的事件列表
                event_list = panel.find('ul', class_='list-group')
                if event_list:
                    events = event_list.find_all('li', class_='list-group-item')
                    
                    for event in events:
                        event_text = event.get_text(strip=True)
                        
                        result = {
                            'rank': "",  # 财经日历没有排名
                            'title': event_text,
                            'link': "",  # 财经日历没有链接
                            'publish_time': date_text,
                            'heat': "",  # 财经日历没有热度
                            'type': '财经日历',
                            'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        results.append(result)
                else:
                    logging.warning(f"未找到日期 {date_text} 的事件列表")
                    
        except Exception as e:
            logging.error(f"解析财经日历失败: {e}")
        
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
            logging.info(f"开始获取 {type_name}...")
            results = self.get_hot_news(type_key)
            all_results[type_name] = results
            logging.info(f"获取到 {type_name} {len(results)} 条数据")
            time.sleep(random.uniform(1, 3))  # 随机等待时间，避免请求过于频繁
        
        total_count = sum(len(items) for items in all_results.values())
        logging.info(f"总共获取到 {total_count} 条热点数据")
        
        return all_results
    
    def save_to_file(self, data, filename=None):
        """保存数据到JSON文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hotspot_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"数据已保存到JSON: {filename}")
            return filename
        except Exception as e:
            logging.error(f"保存JSON文件失败: {e}")
            return None
    
    def save_to_csv(self, data, filename=None):
        """保存数据到CSV文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hotspot_data_{timestamp}.csv"
        
        try:
            import csv
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(['类型', '排名', '标题', '链接', '发布时间', '热度', '抓取时间'])
                
                # 写入数据
                for category, items in data.items():
                    for item in items:
                        writer.writerow([
                            category,
                            item.get('rank', ''),
                            item.get('title', ''),
                            item.get('link', ''),
                            item.get('publish_time', ''),
                            item.get('heat', ''),
                            item.get('crawl_time', '')
                        ])
            
            logging.info(f"数据已导出到CSV: {filename}")
            return filename
        except Exception as e:
            logging.error(f"导出CSV失败: {e}")
            return None

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