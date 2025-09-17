import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_api_endpoints():
    """测试所有API端点"""
    print("测试API端点...")
    print("=" * 50)
    
    # 测试首页
    print("1. 测试首页...")
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("   ✅ 首页API正常")
    else:
        print(f"   ❌ 首页API异常: {response.status_code}")
    
    # 测试热点资讯
    print("2. 测试热点资讯...")
    response = requests.get(f"{BASE_URL}/api/hot_news?limit=3")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 热点资讯API正常, 返回 {data['count']} 条数据")
    else:
        print(f"   ❌ 热点资讯API异常: {response.status_code}")
    
    # 测试今日热点
    print("3. 测试今日热点...")
    response = requests.get(f"{BASE_URL}/api/today_hotspot?limit=3")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 今日热点API正常, 返回 {data['count']} 条数据")
    else:
        print(f"   ❌ 今日热点API异常: {response.status_code}")
    
    # 测试财经日历
    print("4. 测试财经日历...")
    response = requests.get(f"{BASE_URL}/api/financial_calendar?limit=3")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ 财经日历API正常, 返回 {data['count']} 条数据")
    else:
        print(f"   ❌ 财经日历API异常: {response.status_code}")
        print(f"   响应内容: {response.text}")
    
    # 测试数据统计
    print("5. 测试数据统计...")
    response = requests.get(f"{BASE_URL}/api/statistics")
    if response.status_code == 200:
        data = response.json()
        total = data['data']['总计']
        print(f"   ✅ 数据统计API正常, 总计 {total} 条数据")
    else:
        print(f"   ❌ 数据统计API异常: {response.status_code}")
    
    print("=" * 50)
    print("API测试完成！")

def show_api_documentation():
    """显示API文档"""
    print("\nAPI使用说明:")
    print("=" * 50)
    print("1. 首页: GET /")
    print("2. 热点资讯: GET /api/hot_news?limit=10&type=热点资讯")
    print("3. 公社热帖: GET /api/hot_news?limit=10&type=公社热帖")
    print("4. 今日热点: GET /api/today_hotspot?limit=10")
    print("5. 财经日历: GET /api/financial_calendar?limit=10&date=2025-09-17")
    print("6. 数据统计: GET /api/statistics")
    print("7. 搜索: GET /api/search?q=关键词&limit=10")
    print("\n示例:")
    print("curl http://127.0.0.1:5000/api/hot_news?limit=5")
    print("curl http://127.0.0.1:5000/api/today_hotspot?limit=3")
    print("curl http://127.0.0.1:5000/api/statistics")

if __name__ == "__main__":
    try:
        test_api_endpoints()
        show_api_documentation()
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器，请确保api_server.py正在运行")
        print("运行命令: python api_server.py")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")