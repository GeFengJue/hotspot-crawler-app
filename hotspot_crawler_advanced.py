import requests
import json
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging
import schedule

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hotspot_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class AdvancedHotSpotCrawler:
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
    
    def get_hot_news(self, news_type, retry_count=3):
        """获取热点新闻，支持重试机制"""
        url = f"{self.base_url}/api/getHotNewsByType"
        payload = {'type': news_type}
        
        # 特殊处理财经日历
        if news_type == 'timeline':
            return self.get_timeline_data(retry_count)
        
        for attempt in range(retry_count):
            try:
                response = self.session.post(url, data=payload, timeout=15)
                response.raise_for_status()
                
                data = response.json()
                if data.get('result') == 'success':
                    return self.parse_hot_news(data.get('html', ''), news_type)
                else:
                    logging.warning(f"获取{news_type}数据失败: {data}")
                    return []
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"第{attempt + 1}次请求失败: {str(e)}")
                if attempt < retry_count - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    return f"请求错误: {str(e)}"
            except json.JSONDecodeError as e:
                logging.error(f"JSON解析错误: {str(e)}")
                return f"数据解析错误: {str(e)}"

    def get_timeline_data(self, retry_count=3):
        """获取财经日历数据"""
        logging.info("尝试获取财经日历数据...")
        # 财经日历可能需要不同的API或参数
        # 先尝试直接访问页面获取数据
        try:
            response = self.session.get(f"{self.base_url}/web/hotnews/web", timeout=15)
            response.raise_for_status()
            
            # 从HTML中解析财经日历数据
            soup = BeautifulSoup(response.text, 'html.parser')
            timeline_data = self.parse_timeline_from_html(soup)
            
            if timeline_data:
                return timeline_data
            else:
                logging.warning("未找到财经日历数据")
                return []
                
        except Exception as e:
            logging.error(f"获取财经日历失败: {str(e)}")
            return []

    def parse_timeline_from_html(self, soup):
        """从HTML中解析财经日历数据"""
        # 这里需要根据实际页面结构来解析
        # 由于页面结构复杂，可能需要更精细的解析
        timeline_items = []
        
        # 尝试查找财经日历相关的元素
        # 这里只是一个示例，需要根据实际页面调整
        calendar_elements = soup.find_all('div', class_=re.compile('calendar|timeline'))
        
        if not calendar_elements:
            logging.warning("未找到财经日历元素")
            return []
        
        # 具体的解析逻辑需要根据实际HTML结构来写
        logging.info(f"找到{len(calendar_elements)}个日历元素")
        return timeline_items
    
    def parse_hot_news(self, html_content, news_type):
        """解析HTML内容"""
        if not html_content:
            return []
            
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
                    'heat': int(heat) if heat.isdigit() else 0,
                    'type': news_type,
                    'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                results.append(result)
                
            except Exception as e:
                logging.error(f"解析项目时出错: {e}")
                continue
        
        return results
    
    def get_all_hotspots(self):
        """获取所有类型的热点内容"""
        hotspot_types = {
            'ths': '热点资讯',
            'chaosha': '今日热点', 
            'jiuyan': '公社热帖',
            'timeline': '财经日历',
            'ths_hot': '同花热榜'
        }
        
        all_results = {}
        total_count = 0
        
        for type_key, type_name in hotspot_types.items():
            logging.info(f"正在获取{type_name}...")
            results = self.get_hot_news(type_key)
            
            if isinstance(results, list):
                all_results[type_name] = results
                total_count += len(results)
                logging.info(f"获取到{type_name} {len(results)}条数据")
            else:
                logging.error(f"获取{type_name}失败: {results}")
                all_results[type_name] = []
            
            time.sleep(1)  # 礼貌等待
        
        logging.info(f"总共获取到{total_count}条热点数据")
        return all_results
    
    def save_to_file(self, data, filename=None):
        """保存数据到JSON文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hotspot_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"数据已保存到: {filename}")
            return filename
        except Exception as e:
            logging.error(f"保存文件失败: {e}")
            return None
    
    def export_to_csv(self, data, filename=None):
        """导出数据到CSV文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hotspot_data_{timestamp}.csv"
        
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                # 写入表头
                writer.writerow(['类型', '排名', '标题', '链接', '发布时间', '热度', '抓取时间'])
                
                # 写入数据
                for category, items in data.items():
                    for item in items:
                        writer.writerow([
                            category,
                            item['rank'],
                            item['title'],
                            item['link'],
                            item['publish_time'],
                            item['heat'],
                            item['crawl_time']
                        ])
            
            logging.info(f"数据已导出到CSV: {filename}")
            return filename
        except Exception as e:
            logging.error(f"导出CSV失败: {e}")
            return None

def scheduled_crawl():
    """定时抓取任务"""
    crawler = AdvancedHotSpotCrawler()
    
    logging.info("开始定时抓取热点数据...")
    all_data = crawler.get_all_hotspots()
    
    # 保存数据
    json_file = crawler.save_to_file(all_data)
    csv_file = crawler.export_to_csv(all_data)
    
    # 打印摘要
    for category, items in all_data.items():
        if items:
            print(f"\n=== {category} ({len(items)}条) ===")
            for i, item in enumerate(items[:3], 1):  # 只显示前3条
                print(f"{i}. {item['title'][:50]}... (热度: {item['heat']})")

def main():
    """主函数"""
    print("高级热点数据抓取工具")
    print("=" * 50)
    
    crawler = AdvancedHotSpotCrawler()
    
    # 获取所有热点数据
    all_data = crawler.get_all_hotspots()
    
    # 保存数据
    json_file = crawler.save_to_file(all_data)
    csv_file = crawler.export_to_csv(all_data)
    
    # 打印结果摘要
    print("\n抓取结果摘要:")
    print("=" * 50)
    for category, items in all_data.items():
        count = len(items)
        if count > 0:
            heat_sum = sum(item['heat'] for item in items)
            print(f"{category}: {count}条数据, 总热度: {heat_sum}")
        else:
            print(f"{category}: 无数据")
    
    print(f"\n数据文件已生成:")
    if json_file:
        print(f"  JSON: {json_file}")
    if csv_file:
        print(f"  CSV: {csv_file}")

if __name__ == "__main__":
    main()