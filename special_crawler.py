import requests
import json
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SpecialHotSpotCrawler:
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
    
    def get_today_hotspot(self):
        """获取今日热点数据"""
        logging.info("尝试获取今日热点数据...")
        
        try:
            # 模拟点击今日热点按钮
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
                    return self.parse_today_hotspot_from_html(html_content)
                else:
                    logging.warning("今日热点返回空HTML内容")
                    return []
            else:
                logging.warning(f"今日热点API返回失败: {data}")
                return []
                
        except Exception as e:
            logging.error(f"获取今日热点失败: {str(e)}")
            return []

    def parse_today_hotspot_from_html(self, html_content):
        """从HTML内容解析今日热点"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        try:
            # 解析今日热点面板
            chaosha_panel = soup.find('div', id='chaosha')
            if not chaosha_panel:
                logging.warning("未找到今日热点面板")
                return []
            
            # 解析日期
            date_div = chaosha_panel.find('div', class_='panel-heading')
            date_text = date_div.get_text(strip=True) if date_div else ""
            
            # 解析关键词和热度
            info_div = chaosha_panel.find('div', style="color:#999;")
            if info_div:
                keyword_text = info_div.get_text(strip=True)
            else:
                keyword_text = ""
            
            # 解析热点标题
            keyword_div = chaosha_panel.find('div', class_='keyword')
            if keyword_div:
                title_b = keyword_div.find('b')
                title = title_b.get_text(strip=True) if title_b else keyword_div.get_text(strip=True)
                
                result = {
                    'date': date_text,
                    'keywords': keyword_text,
                    'title': title,
                    'type': '今日热点',
                    'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                results.append(result)
            else:
                logging.warning("未找到今日热点标题")
                
        except Exception as e:
            logging.error(f"解析今日热点失败: {e}")
        
        return results
    
    def parse_today_hotspot(self, soup):
        """解析今日热点数据"""
        results = []
        
        # 根据用户提供的HTML结构解析今日热点
        try:
            # 查找今日热点面板
            chaosha_panel = soup.find('div', id='chaosha')
            if not chaosha_panel:
                logging.warning("未找到今日热点面板")
                return []
            
            # 解析日期
            date_div = chaosha_panel.find('div', class_='panel-heading')
            date_text = date_div.get_text(strip=True) if date_div else ""
            
            # 解析关键词和热度
            info_div = chaosha_panel.find('div', style="color:#999;")
            if info_div:
                keyword_text = info_div.get_text(strip=True)
            else:
                keyword_text = ""
            
            # 解析热点标题
            keyword_div = chaosha_panel.find('div', class_='keyword')
            if keyword_div:
                title_b = keyword_div.find('b')
                title = title_b.get_text(strip=True) if title_b else keyword_div.get_text(strip=True)
                
                result = {
                    'date': date_text,
                    'keywords': keyword_text,
                    'title': title,
                    'type': '今日热点',
                    'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                results.append(result)
            else:
                logging.warning("未找到今日热点标题")
                
        except Exception as e:
            logging.error(f"解析今日热点失败: {e}")
        
        return results

    def parse_calendar(self, soup):
        """解析财经日历数据"""
        results = []
        
        # 根据用户提供的HTML结构解析财经日历
        try:
            # 查找财经日历面板
            calendar_panel = soup.find('div', id='timeline')
            if not calendar_panel:
                logging.warning("未找到财经日历面板")
                return []
            
            # 解析日期标题
            date_div = calendar_panel.find('div', class_='panel-heading')
            date_text = date_div.get_text(strip=True) if date_div else ""
            
            # 解析日历事件列表
            event_list = calendar_panel.find('ul', class_='list-group')
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
                logging.warning("未找到财经日历事件列表")
                
        except Exception as e:
            logging.error(f"解析财经日历失败: {e}")
        
        return results
    
    def get_financial_calendar(self):
        """获取财经日历数据"""
        logging.info("尝试获取财经日历数据...")
        
        try:
            # 模拟点击财经日历按钮
            response = self.session.post(
                f"{self.base_url}/api/getHotNewsByType",
                data={'type': 'timeline'},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            logging.info(f"财经日历API响应: result={data.get('result')}, html_length={len(data.get('html', '')) if data.get('html') else 0}")
            
            if data.get('result') == 'success':
                html_content = data.get('html', '')
                cdate = data.get('cdate', '')
                
                if html_content:
                    logging.info(f"财经日历HTML内容长度: {len(html_content)}")
                    return self.parse_calendar_from_html(html_content, cdate)
                else:
                    logging.warning("财经日历返回空HTML内容")
                    return []
            else:
                logging.warning(f"财经日历API返回失败: {data}")
                return []
                
        except Exception as e:
            logging.error(f"获取财经日历失败: {str(e)}")
            return []

    def parse_calendar_from_html(self, html_content, cdate):
        """从HTML内容解析财经日历"""
        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        try:
            # 解析所有panel元素（每个panel代表一个日期）
            panels = soup.find_all('div', class_='panel panel-danger')
            logging.info(f"找到 {len(panels)} 个财经日历面板")
            
            for panel in panels:
                # 提取日期标题
                date_heading = panel.find('div', class_='panel-heading')
                date_text = date_heading.get_text(strip=True) if date_heading else ""
                logging.info(f"处理日期: {date_text}")
                
                # 提取该日期下的事件列表
                event_list = panel.find('ul', class_='list-group')
                if event_list:
                    events = event_list.find_all('li', class_='list-group-item')
                    logging.info(f"找到 {len(events)} 个事件")
                    
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
        
        logging.info(f"财经日历解析完成，共 {len(results)} 条记录")
        return results
    
    def simulate_calendar_click(self):
        """模拟点击财经日历按钮"""
        logging.info("尝试模拟点击财经日历...")
        
        try:
            # 发送模拟点击的请求
            response = self.session.post(
                f"{self.base_url}/api/getHotNewsByType",
                data={'type': 'timeline'},
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('result') == 'success':
                # 财经日历返回的数据可能包含日期信息
                cdate = data.get('cdate', '')
                html_content = data.get('html', '')
                
                if html_content:
                    return self.parse_calendar_from_html(html_content, cdate)
                else:
                    logging.warning("财经日历返回空HTML内容")
                    return []
            else:
                logging.warning(f"财经日历API返回失败: {data}")
                return []
                
        except Exception as e:
            logging.error(f"模拟点击财经日历失败: {str(e)}")
            return []
    
    def parse_calendar(self, soup):
        """解析财经日历数据"""
        # 这里需要根据实际页面结构来解析财经日历
        # 由于页面结构复杂，返回空数组
        return []
    
    def get_all_special_data(self):
        """获取所有特殊类型的数据"""
        results = {
            '今日热点': self.get_today_hotspot(),
            '财经日历': self.get_financial_calendar()
        }
        
        return results
    
    def save_to_file(self, data, filename=None):
        """保存数据到文件"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"special_data_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f"特殊数据已保存到: {filename}")
            return filename
        except Exception as e:
            logging.error(f"保存文件失败: {e}")
            return None

def main():
    """主函数"""
    print("特殊数据抓取工具 - 今日热点和财经日历")
    print("=" * 50)
    
    crawler = SpecialHotSpotCrawler()
    
    # 获取特殊数据
    special_data = crawler.get_all_special_data()
    
    # 打印结果
    for category, items in special_data.items():
        count = len(items)
        print(f"\n=== {category} ({count}条) ===")
        
        if count > 0:
            for i, item in enumerate(items[:5], 1):  # 只显示前5条
                if category == '今日热点':
                    print(f"{i}. {item['title']}")
                    if 'content' in item:
                        print(f"   内容: {item['content'][:100]}...")
                elif category == '财经日历':
                    print(f"{i}. {item['date']} - {item['event']}")
        else:
            print("无数据")
    
    # 保存到文件
    filename = crawler.save_to_file(special_data)
    if filename:
        print(f"\n数据已保存到: {filename}")

if __name__ == "__main__":
    main()