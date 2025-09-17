import sqlite3
import json
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseManager:
    def __init__(self, db_name='hotspot_data.db'):
        self.db_name = db_name
        self.conn = None
        self.create_tables()
    
    def connect(self):
        """连接到数据库"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
            logging.info(f"成功连接到数据库: {self.db_name}")
            return True
        except sqlite3.Error as e:
            logging.error(f"数据库连接失败: {e}")
            return False
    
    def create_tables(self):
        """创建数据表"""
        if not self.connect():
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # 热点资讯表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hot_news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rank TEXT,
                    title TEXT NOT NULL,
                    link TEXT,
                    publish_time TEXT,
                    heat TEXT,
                    type TEXT NOT NULL,
                    crawl_time TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 今日热点表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS today_hotspot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    title TEXT NOT NULL,
                    keywords TEXT,
                    heat TEXT,
                    type TEXT NOT NULL,
                    crawl_time TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 财经日历表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS financial_calendar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    event TEXT NOT NULL,
                    type TEXT NOT NULL,
                    crawl_time TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            logging.info("数据表创建成功")
            return True
            
        except sqlite3.Error as e:
            logging.error(f"创建数据表失败: {e}")
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def insert_hot_news(self, data):
        """插入热点资讯数据"""
        if not self.connect():
            return False
        
        try:
            cursor = self.conn.cursor()
            
            for item in data:
                cursor.execute('''
                    INSERT INTO hot_news (rank, title, link, publish_time, heat, type, crawl_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item.get('rank', ''),
                    item.get('title', ''),
                    item.get('link', ''),
                    item.get('publish_time', ''),
                    item.get('heat', ''),
                    item.get('type', ''),
                    item.get('crawl_time', '')
                ))
            
            self.conn.commit()
            logging.info(f"成功插入 {len(data)} 条热点资讯数据")
            return True
            
        except sqlite3.Error as e:
            logging.error(f"插入热点资讯数据失败: {e}")
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def insert_today_hotspot(self, data):
        """插入今日热点数据"""
        if not self.connect():
            return False
        
        try:
            cursor = self.conn.cursor()
            
            for item in data:
                cursor.execute('''
                    INSERT INTO today_hotspot (date, title, keywords, heat, type, crawl_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    item.get('date', ''),
                    item.get('title', ''),
                    item.get('keywords', ''),
                    item.get('heat', ''),
                    item.get('type', ''),
                    item.get('crawl_time', '')
                ))
            
            self.conn.commit()
            logging.info(f"成功插入 {len(data)} 条今日热点数据")
            return True
            
        except sqlite3.Error as e:
            logging.error(f"插入今日热点数据失败: {e}")
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def insert_financial_calendar(self, data):
        """插入财经日历数据"""
        if not self.connect():
            return False
        
        try:
            cursor = self.conn.cursor()
            
            for item in data:
                cursor.execute('''
                    INSERT INTO financial_calendar (date, event, type, crawl_time)
                    VALUES (?, ?, ?, ?)
                ''', (
                    item.get('date', ''),
                    item.get('event', ''),
                    item.get('type', ''),
                    item.get('crawl_time', '')
                ))
            
            self.conn.commit()
            logging.info(f"成功插入 {len(data)} 条财经日历数据")
            return True
            
        except sqlite3.Error as e:
            logging.error(f"插入财经日历数据失败: {e}")
            return False
        finally:
            if self.conn:
                self.conn.close()
    
    def import_from_json(self, json_file):
        """从JSON文件导入数据"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 插入热点资讯数据
            if '热点资讯' in data:
                self.insert_hot_news(data['热点资讯'])
            
            # 插入公社热帖数据（也存入热点资讯表，类型不同）
            if '公社热帖' in data:
                jiuyan_data = data['公社热帖']
                for item in jiuyan_data:
                    item['type'] = '公社热帖'
                self.insert_hot_news(jiuyan_data)
            
            # 插入今日热点数据
            if '今日热点' in data:
                self.insert_today_hotspot(data['今日热点'])
            
            # 插入财经日历数据
            if '财经日历' in data:
                self.insert_financial_calendar(data['财经日历'])
            
            logging.info(f"从 {json_file} 导入数据完成")
            return True
            
        except Exception as e:
            logging.error(f"导入JSON数据失败: {e}")
            return False
    
    def get_hot_news(self, limit=50, news_type=None):
        """获取热点资讯数据"""
        if not self.connect():
            return []
        
        try:
            cursor = self.conn.cursor()
            
            if news_type:
                cursor.execute('''
                    SELECT * FROM hot_news 
                    WHERE type = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (news_type, limit))
            else:
                cursor.execute('''
                    SELECT * FROM hot_news 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append(dict(row))
            
            return results
            
        except sqlite3.Error as e:
            logging.error(f"获取热点资讯数据失败: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()
    
    def get_today_hotspot(self, limit=20):
        """获取今日热点数据"""
        if not self.connect():
            return []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM today_hotspot 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append(dict(row))
            
            return results
            
        except sqlite3.Error as e:
            logging.error(f"获取今日热点数据失败: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()
    
    def get_financial_calendar(self, limit=50, date_filter=None):
        """获取财经日历数据"""
        if not self.connect():
            return []
        
        try:
            cursor = self.conn.cursor()
            
            if date_filter:
                cursor.execute('''
                    SELECT * FROM financial_calendar 
                    WHERE date = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (date_filter, limit))
            else:
                cursor.execute('''
                    SELECT * FROM financial_calendar 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                results.append(dict(row))
            
            return results
            
        except sqlite3.Error as e:
            logging.error(f"获取财经日历数据失败: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()
    
    def get_data_statistics(self):
        """获取数据统计信息"""
        if not self.connect():
            return {}
        
        try:
            cursor = self.conn.cursor()
            
            statistics = {}
            
            # 热点资讯统计
            cursor.execute('SELECT COUNT(*) as count, type FROM hot_news GROUP BY type')
            for row in cursor.fetchall():
                statistics[row['type']] = row['count']
            
            # 今日热点统计
            cursor.execute('SELECT COUNT(*) as count FROM today_hotspot')
            statistics['今日热点'] = cursor.fetchone()['count']
            
            # 财经日历统计
            cursor.execute('SELECT COUNT(*) as count FROM financial_calendar')
            statistics['财经日历'] = cursor.fetchone()['count']
            
            # 总数据量
            total = sum(statistics.values())
            statistics['总计'] = total
            
            return statistics
            
        except sqlite3.Error as e:
            logging.error(f"获取数据统计失败: {e}")
            return {}
        finally:
            if self.conn:
                self.conn.close()

def main():
    """主函数"""
    print("数据库管理工具")
    print("=" * 50)
    
    # 创建数据库管理器
    db_manager = DatabaseManager()
    
    # 导入最新的JSON数据
    json_file = "complete_hotspot_data_20250917_173619.json"
    db_manager.import_from_json(json_file)
    
    # 显示数据统计
    stats = db_manager.get_data_statistics()
    print("\n=== 数据统计 ===")
    for key, value in stats.items():
        print(f"{key}: {value}条")
    
    print(f"\n数据库文件: hotspot_data.db")
    print("数据已成功导入数据库，可用于后续API开发")

if __name__ == "__main__":
    main()