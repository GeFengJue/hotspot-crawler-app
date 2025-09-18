#!/usr/bin/env python3
"""
更新热点数据文件脚本
将最新的数据文件复制为固定名称供前端使用
"""

import os
import glob
import shutil
from datetime import datetime

def get_latest_data_file():
    """获取最新的数据文件"""
    json_files = glob.glob("hotspot_data_*.json")
    if not json_files:
        return None
    
    # 按修改时间排序，获取最新的文件
    latest_file = max(json_files, key=os.path.getmtime)
    return latest_file

def update_hotspot_data():
    """更新热点数据文件"""
    print("正在更新热点数据文件...")
    
    # 获取最新的数据文件
    latest_file = get_latest_data_file()
    if not latest_file:
        print("未找到数据文件")
        return False
    
    print(f"找到最新数据文件: {latest_file}")
    
    # 复制为固定名称
    try:
        shutil.copy2(latest_file, "hotspot_data.json")
        print(f"已更新: hotspot_data.json")
        
        # 验证文件内容
        if os.path.exists("hotspot_data.json") and os.path.getsize("hotspot_data.json") > 100:
            print("✅ 热点数据文件更新成功")
            return True
        else:
            print("❌ 热点数据文件更新失败")
            return False
            
    except Exception as e:
        print(f"❌ 复制文件时出错: {e}")
        return False

if __name__ == "__main__":
    success = update_hotspot_data()
    exit(0 if success else 1)