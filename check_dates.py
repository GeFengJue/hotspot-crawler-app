import sqlite3

def check_today_hotspot_dates():
    conn = sqlite3.connect('hotspot_data.db')
    cursor = conn.cursor()
    
    # 查询今日热点数据的日期分布
    cursor.execute('SELECT DISTINCT date FROM hotspot_data WHERE type=? ORDER BY date DESC', ('今日热点',))
    dates = cursor.fetchall()
    
    print('今日热点可用日期:')
    for date in dates:
        print(date[0])
    
    # 查询每个日期的数据条数
    for date in dates:
        cursor.execute('SELECT COUNT(*) FROM hotspot_data WHERE type=? AND date=?', ('今日热点', date[0]))
        count = cursor.fetchone()[0]
        print(f'日期 {date[0]} 有 {count} 条数据')
    
    conn.close()

if __name__ == '__main__':
    check_today_hotspot_dates()