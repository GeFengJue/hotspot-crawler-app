#!/usr/bin/env python3
"""
部署检查脚本 - 验证所有服务正常运行
"""

import requests
import time
import subprocess
import sys
import os

def check_api_server():
    """检查API服务器是否正常运行"""
    try:
        response = requests.get('http://127.0.0.1:5000/api/hot_news', timeout=5)
        if response.status_code == 200:
            print("✅ API服务器正常运行")
            return True
        else:
            print(f"❌ API服务器返回错误状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API服务器连接失败: {e}")
        return False

def check_static_server():
    """检查静态服务器是否正常运行"""
    # 尝试多个可能的端口
    ports = [9000, 9001, 9002, 8080, 8081]
    
    for port in ports:
        try:
            response = requests.get(f'http://127.0.0.1:{port}/index.html', timeout=3)
            if response.status_code == 200:
                print(f"✅ 静态服务器正常运行 (端口: {port})")
                return True
        except requests.exceptions.RequestException:
            continue
    
    print("❌ 静态服务器连接失败，请手动启动: python static_server.py [端口号]")
    return False

def check_database():
    """检查数据库文件是否存在"""
    db_file = 'hotspot_data.db'
    if os.path.exists(db_file):
        file_size = os.path.getsize(db_file)
        print(f"✅ 数据库文件存在，大小: {file_size} 字节")
        return True
    else:
        print("❌ 数据库文件不存在")
        return False

def run_crawler_test():
    """测试爬虫功能"""
    try:
        result = subprocess.run([
            sys.executable, 'complete_hotspot_crawler.py'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ 爬虫测试执行成功")
            return True
        else:
            print(f"❌ 爬虫测试失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ 爬虫测试超时")
        return False
    except Exception as e:
        print(f"❌ 爬虫测试异常: {e}")
        return False

def main():
    """主检查函数"""
    print("=" * 60)
    print("热点资讯爬虫应用 - 部署检查")
    print("=" * 60)
    
    checks = [
        ("API服务器检查", check_api_server),
        ("静态服务器检查", check_static_server),
        ("数据库检查", check_database),
        ("爬虫功能检查", run_crawler_test)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n🔍 正在执行: {check_name}")
        result = check_func()
        results.append(result)
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("检查结果汇总:")
    print("=" * 60)
    
    success_count = sum(results)
    total_count = len(results)
    
    for i, (check_name, _) in enumerate(checks):
        status = "✅" if results[i] else "❌"
        print(f"{status} {check_name}")
    
    print(f"\n总计: {success_count}/{total_count} 项检查通过")
    
    if success_count == total_count:
        print("\n🎉 所有检查通过！应用部署成功！")
        print("\n访问地址:")
        print("前端界面: http://localhost:9000/index.html")
        print("API接口: http://localhost:5000/api/hot_news")
    else:
        print("\n⚠️  部分检查未通过，请检查相关服务")
    
    print("=" * 60)

if __name__ == "__main__":
    main()