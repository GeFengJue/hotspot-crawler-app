import sqlite3

def check_today_hotspot_dates():
    conn = sqlite3.connect('hotspot_data.db')
    cursor = conn.cursor()
    
    # 查询今日热点数据的日期分布
    cursor.execute('SELECT DISTINCT date FROM today_hotspot ORDER BY date DESC')
    dates = cursor.fetchall()
    
    print('今日热点可用日期:')
    for date in dates:
        print(date[0])
    
    # 查询每个日期的数据条数
    for date in dates:
        cursor.execute('SELECT COUNT(*) FROM today_hotspot WHERE date=?', (date[0],))
        count = cursor.fetchone()[0]
        print(f'日期 {date[0]} 有 {count} 条数据')
        
        # 显示该日期的前几条数据
        cursor.execute('SELECT title, keywords, heat FROM today_hotspot WHERE date=? LIMIT 3', (date[0],))
        items = cursor.fetchall()
        for i, item in enumerate(items, 1):
            print(f'  {i}. {item[0]} - 关键词: {item[1]} - 热度: {item[2]}')
        print()
    
    conn.close()

if __name__ == '__main__':
    check_today_hotspot_dates()