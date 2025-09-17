import time
import schedule
import subprocess
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

def run_crawler():
    """运行爬虫任务"""
    try:
        logging.info("开始执行定时爬虫任务...")
        
        # 1. 运行爬虫
        result = subprocess.run(['python', 'complete_hotspot_crawler.py'], 
                               capture_output=True, text=True, cwd='.')
        if result.returncode == 0:
            logging.info("爬虫执行成功")
            
            # 2. 导入数据到数据库
            import_result = subprocess.run(['python', '-c', 
                                          'import database_manager; db = database_manager.DatabaseManager(); '
                                          'db.import_from_json(\"complete_hotspot_data_\" + __import__(\"datetime\").datetime.now().strftime(\"%Y%m%d_%H%M%S\") + \".json\")'],
                                         capture_output=True, text=True, cwd='.')
            if import_result.returncode == 0:
                logging.info("数据导入数据库成功")
            else:
                logging.error(f"数据导入失败: {import_result.stderr}")
                
        else:
            logging.error(f"爬虫执行失败: {result.stderr}")
            
    except Exception as e:
        logging.error(f"定时任务执行异常: {str(e)}")

def main():
    """主函数"""
    logging.info("定时任务调度器启动")
    
    # 每30分钟执行一次
    schedule.every(30).minutes.do(run_crawler)
    
    # 立即执行一次
    run_crawler()
    
    # 保持调度运行
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()