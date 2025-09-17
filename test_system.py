#!/usr/bin/env python3
"""
系统测试脚本 - 测试热点聚焦系统的所有功能
"""

import requests
import json
import time
import sys

def test_api_endpoints():
    """测试所有API端点"""
    base_url = "http://127.0.0.1:5000"
    endpoints = [
        "/api/hot_news",
        "/api/today_hotspot", 
        "/api/financial_calendar",
        "/api/statistics"
    ]
    
    print("=" * 60)
    print("测试热点聚焦系统API端点")
    print("=" * 60)
    
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', len(data.get('data', [])))
                print(f"✅ {endpoint}: 成功 (数据量: {count})")
            else:
                print(f"❌ {endpoint}: 失败 (状态码: {response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: 连接失败 - {e}")
        except json.JSONDecodeError as e:
            print(f"❌ {endpoint}: JSON解析失败 - {e}")
    
    print("=" * 60)

def test_static_server():
    """测试静态文件服务器"""
    base_url = "http://localhost:8080"
    
    print("测试静态文件服务器")
    print("=" * 60)
    
    try:
        response = requests.get(base_url + "/index.html", timeout=10)
        if response.status_code == 200:
            print("✅ 静态服务器: 成功")
            print(f"   前端页面: {base_url}/index.html")
        else:
            print(f"❌ 静态服务器: 失败 (状态码: {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 静态服务器: 连接失败 - {e}")
    
    print("=" * 60)

def main():
    """主测试函数"""
    print("热点聚焦系统测试")
    print("=" * 60)
    
    # 检查API服务器
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ API服务器: 运行中")
        else:
            print("❌ API服务器: 未运行")
            return False
    except:
        print("❌ API服务器: 未运行")
        return False
    
    # 测试API端点
    test_api_endpoints()
    
    # 测试静态服务器
    test_static_server()
    
    print("测试完成！")
    print("=" * 60)
    print("访问地址:")
    print("  API接口: http://127.0.0.1:5000/")
    print("  前端页面: http://localhost:8080/index.html")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()