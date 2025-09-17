import requests
import json
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging
import csv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CompleteHotSpotCrawler:
    def __init__(self):
        self.base_url = "https://duanxianxia.com"
        self.session = requests.Session()
        self.setup_headers()
        
    def setup_headers(self):
        """设置请求头"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Referer': f'{self.base_url}/web/hotnews/web'
        })
    
    def get_hot_news(self, news_type='ths'):
        """获取热点资讯数据"""
        logging.info(f"尝试获取{news_type}热点资讯数据...")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/getHotNewsByType",
                data={'type': news_type},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('result') == 'success':
                html_content = data.get('html', '')
                if html_content:
                    return self.parse_hot_news(html_content, news_type)
                else:
                    logging.warning(f"{news_type}热点资讯返回空HTML内容")
                    return []
            else:
                logging.warning(f"{news_type}热点资讯API返回失败: {data}")
                return []
                
        except Exception as e:
            logging.error(f"获取{news_type}热点资讯失败: {str(e)}")
            return []
    
    def parse_hot_news(self, html_content, news_type):
        """解析热点资讯HTML内容"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        items = soup.find_all('div', class_='item flex')
        
        for item in items:
            try:
                # 提取排名
                no_div = item.find('div', class_='no')
                rank = no_div.get_text(strip=True) if no_div else ""
                
                # 提取标题和链接
                title_link = item.find('a')
                title = title_link.get_text(strip=True) if title_link else ""
                href = title_link.get('href', '') if title_link else ""
                
                if href and not href.startswith('http'):
                    href = f"https:{href}" if href.startswith('//') else href
                
                # 提取时间
                time_span = item.find('span', class_='time')
                publish_time = time_span.get_text(strip=True) if time_span else ""
                
                # 提取热度
                heat_span = item.find('span', style="width:90px;display:inline-block;")
                heat = heat_span.get_text(strip=True).replace('热度：', '') if heat_span else ""
                
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
                logging.error(f"解析热点资讯项目失败: {e}")
                continue
        
        return results
    
    def get_today_hotspot(self):
        """获取今日热点数据"""
        logging.info("尝试获取今日热点数据...")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/getHotNewsByType",
                data={'type': 'chaosha'},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('result') == 'success':
                html_content = data.get('html', '')
                if html_content:
                    return self.parse_today_hotspot(html_content)
                else:
                    logging.warning("今日热点返回空HTML内容")
                    return []
            else:
                logging.warning(f"今日热点API返回失败: {data}")
                return []
                
        except Exception as e:
            logging.error(f"获取今日热点失败: {str(e)}")
            return []
    
    def parse_today_hotspot(self, html_content):
        """解析今日热点内容"""
        soup = BeautifulSoup(html_content, 'html.parser')
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
                
                # 查找该面板内的所有关键词块
                keyword_blocks = panel.find_all('div', class_='keyword')
                
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
                        'date': date_text,
                        'keywords': keyword,
                        'heat': heat,
                        'title': title,
                        'type': '今日热点',
                        'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    results.append(result)
                
        except Exception as e:
            logging.error(f"解析今日热点失败: {e}")
        
        return results
    
    def get_financial_calendar(self):
        """获取财经日历数据"""
        logging.info("尝试获取财经日历数据...")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/getHotNewsByType",
                data={'type': 'timeline'},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('result') == 'success':
                html_content = data.get('html', '')
                cdate = data.get('cdate', '')
                
                if html_content:
                    return self.parse_calendar(html_content, cdate)
                else:
                    logging.warning("财经日历返回空HTML内容")
                    return []
            else:
                logging.warning(f"财经日历API返回失败: {data}")
                return []
                
        except Exception as e:
            logging.error(f"获取财经日历失败: {str(e)}")
            return []
    
    def parse_calendar(self, html_content, cdate):
        """解析财经日历内容"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        try:
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
                            'date': date_text,
                            'event': event_text,
                            'type': '财经日历',
                            'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        results.append(result)
                else:
                    logging.warning(f"未找到日期 {date_text} 的事件列表")
                    
        except Exception as e:
            logging.error(f"解析财经日历失败: {e}")
        
        return results
    
    def get_all_data(self):
        """获取所有类型的数据"""
        results = {
            '热点资讯': self.get_hot_news('ths'),
            '公社热帖': self.get_hot_news('jiuyan'),
            '今日热点': self.get_today_hotspot(),
            '财经日历': self.get_financial_calendar()
        }
        
        return results
    
    def save_to_json(self, data, filename=None):
        """保存数据到JSON文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"complete_hotspot_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"数据已保存到JSON文件: {filename}")
            return filename
        except Exception as e:
            logging.error(f"保存JSON文件失败: {e}")
            return None
    
    def save_to_csv(self, data, filename=None):
        """保存数据到CSV文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"complete_hotspot_data_{timestamp}.csv"
        
        try:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                
                # 写入表头
                writer.writerow(['类型', '排名', '标题', '链接', '发布时间', '热度', '日期', '事件', '关键词', '抓取时间'])
                
                # 写入数据
                for category, items in data.items():
                    for item in items:
                        row = [
                            category,
                            item.get('rank', ''),
                            item.get('title', ''),
                            item.get('link', ''),
                            item.get('publish_time', ''),
                            item.get('heat', ''),
                            item.get('date', ''),
                            item.get('event', ''),
                            item.get('keywords', ''),
                            item.get('crawl_time', '')
                        ]
                        writer.writerow(row)
            
            logging.info(f"数据已保存到CSV文件: {filename}")
            return filename
        except Exception as e:
            logging.error(f"保存CSV文件失败: {e}")
            return None

def main():
    """主函数"""
    print("完整热点数据抓取工具")
    print("=" * 50)
    print("支持抓取: 热点资讯、公社热帖、今日热点、财经日历")
    print("=" * 50)
    
    crawler = CompleteHotSpotCrawler()
    
    # 获取所有数据
    print("开始抓取数据...")
    all_data = crawler.get_all_data()
    
    # 打印统计信息
    total_count = 0
    for category, items in all_data.items():
        count = len(items)
        total_count += count
        print(f"{category}: {count}条")
    
    print(f"\n总计: {total_count}条数据")
    
    # 保存数据
    json_file = crawler.save_to_json(all_data)
    csv_file = crawler.save_to_csv(all_data)
    
    if json_file and csv_file:
        print(f"\n数据已保存到:")
        print(f"JSON文件: {json_file}")
        print(f"CSV文件: {csv_file}")
        
        # 显示部分数据预览
        print(f"\n=== 数据预览 (前3条) ===")
        for category, items in all_data.items():
            if items:
                print(f"\n{category}:")
                for i, item in enumerate(items[:3], 1):
                    if category in ['热点资讯', '公社热帖']:
                        print(f"  {i}. [{item['rank']}] {item['title']} (热度: {item['heat']})")
                        print(f"     链接: {item['link']}")
                    elif category == '今日热点':
                        print(f"  {i}. {item['title']}")
                        print(f"     关键词: {item['keywords']}")
                    elif category == '财经日历':
                        print(f"  {i}. {item['date']} - {item['event']}")

if __name__ == "__main__":
    main()