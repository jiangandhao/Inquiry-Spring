#!/usr/bin/env python3
"""
测试新的API结构
验证按照Django最佳实践重组后的API是否正常工作
"""

import requests
import json
import sys
from datetime import datetime

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_api_endpoint(url, description):
    """测试API端点"""
    try:
        print(f"\n测试: {description}")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 成功")
            return True
        else:
            print(f"❌ 失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 连接错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def main():
    print("🚀 测试新的API结构")
    print(f"📅 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 基础URL: {BASE_URL}")
    
    # 检查服务器连接
    try:
        response = requests.get(f"{BASE_URL}/admin/", timeout=5)
        print("✅ 服务器连接正常")
    except:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
        sys.exit(1)
    
    success_count = 0
    total_tests = 0
    
    # 测试主API端点
    print("\n" + "="*60)
    print(" 主API端点测试")
    print("="*60)
    
    tests = [
        (f"{BASE_URL}/api/", "主API根视图"),
        (f"{BASE_URL}/api/health/", "API健康检查"),
    ]
    
    for url, desc in tests:
        total_tests += 1
        if test_api_endpoint(url, desc):
            success_count += 1
    
    # 测试新版本化API端点
    print("\n" + "="*60)
    print(" 版本化API端点测试 (v1)")
    print("="*60)
    
    v1_tests = [
        (f"{BASE_URL}/api/v1/chat/", "Chat API根视图"),
        (f"{BASE_URL}/api/v1/chat/conversations/", "Chat对话列表"),
        (f"{BASE_URL}/api/v1/documents/", "Documents API根视图"),
        (f"{BASE_URL}/api/v1/documents/documents/", "Documents文档列表"),
        (f"{BASE_URL}/api/v1/quiz/", "Quiz API根视图"),
        (f"{BASE_URL}/api/v1/quiz/quizzes/", "Quiz测验列表"),
    ]
    
    for url, desc in v1_tests:
        total_tests += 1
        if test_api_endpoint(url, desc):
            success_count += 1
    
    # 测试兼容性API端点
    print("\n" + "="*60)
    print(" 兼容性API端点测试 (旧版)")
    print("="*60)
    
    legacy_tests = [
        (f"{BASE_URL}/chat/api/conversations/", "Chat兼容性API"),
        (f"{BASE_URL}/documents/api/documents/", "Documents兼容性API"),
        (f"{BASE_URL}/quiz/api/quizzes/", "Quiz兼容性API"),
    ]
    
    for url, desc in legacy_tests:
        total_tests += 1
        if test_api_endpoint(url, desc):
            success_count += 1
    
    # 测试应用根视图
    print("\n" + "="*60)
    print(" 应用根视图测试")
    print("="*60)
    
    app_root_tests = [
        (f"{BASE_URL}/chat/", "Chat应用根视图"),
        (f"{BASE_URL}/documents/", "Documents应用根视图"),
        (f"{BASE_URL}/quiz/", "Quiz应用根视图"),
    ]
    
    for url, desc in app_root_tests:
        total_tests += 1
        if test_api_endpoint(url, desc):
            success_count += 1
    
    # 显示测试结果
    print("\n" + "="*60)
    print(" 测试结果总结")
    print("="*60)
    
    print(f"✅ 成功: {success_count}/{total_tests}")
    print(f"❌ 失败: {total_tests - success_count}/{total_tests}")
    print(f"📊 成功率: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("\n🎉 所有API端点测试通过！")
        print("📋 新的API结构已成功实现：")
        print("   ✓ 版本化API路径 (/api/v1/)")
        print("   ✓ 应用分离的API结构")
        print("   ✓ 向后兼容性支持")
        print("   ✓ API根视图和健康检查")
    else:
        print(f"\n⚠️  有 {total_tests - success_count} 个端点测试失败")
        print("请检查服务器日志和URL配置")
    
    print("\n💡 推荐的API访问地址：")
    print(f"   📖 主API概览: {BASE_URL}/api/")
    print(f"   📖 Chat API: {BASE_URL}/api/v1/chat/")
    print(f"   📖 Documents API: {BASE_URL}/api/v1/documents/")
    print(f"   📖 Quiz API: {BASE_URL}/api/v1/quiz/")

if __name__ == "__main__":
    main()
