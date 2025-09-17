import sqlite3

def check_database_tables():
    conn = sqlite3.connect('hotspot_data.db')
    cursor = conn.cursor()
    
    # 查询所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print('数据库中的表:')
    for table in tables:
        print(f'表名: {table[0]}')
        
        # 查询表结构
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        print('  列结构:')
        for col in columns:
            print(f'    {col[1]} ({col[2]})')
        print()
    
    conn.close()

if __name__ == '__main__':
    check_database_tables()