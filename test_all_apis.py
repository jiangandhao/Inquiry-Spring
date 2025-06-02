#!/usr/bin/env python
"""
问泉项目完整API测试脚本
测试Chat、Documents、Quiz三个应用的所有API接口
"""
import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = 'http://127.0.0.1:8000'

def print_section(title):
    """打印章节标题"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_response(response, title="响应"):
    """格式化打印响应"""
    print(f"\n{title}:")
    print(f"状态码: {response.status_code}")
    if response.status_code in [200, 201]:
        try:
            data = response.json()
            print(f"数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return data
        except:
            print(f"内容: {response.text}")
    else:
        print(f"错误: {response.text}")
    return None

def test_chat_apis():
    """测试Chat应用API"""
    print_section("1. Chat应用API测试")
    
    # 1.1 测试对话管理
    print("\n1.1 对话管理API")
    
    # 获取对话列表
    response = requests.get(f"{BASE_URL}/chat/api/conversations/")
    print_response(response, "获取对话列表")
    
    # 创建新对话
    conv_data = {
        "title": "API测试对话",
        "mode": "chat",
        "context": "通过API创建的测试对话"
    }
    response = requests.post(f"{BASE_URL}/chat/api/conversations/", json=conv_data)
    conv = print_response(response, "创建新对话")
    
    if conv and 'id' in conv:
        conv_id = conv['id']
        
        # 获取对话详情
        response = requests.get(f"{BASE_URL}/chat/api/conversations/{conv_id}/")
        print_response(response, "获取对话详情")
        
        # 发送消息
        msg_data = {
            "content": "这是一条测试消息",
            "is_user": True
        }
        response = requests.post(f"{BASE_URL}/chat/api/conversations/{conv_id}/messages/", json=msg_data)
        print_response(response, "发送用户消息")
        
        # 发送AI回复
        ai_msg_data = {
            "content": "这是AI的回复消息",
            "is_user": False
        }
        response = requests.post(f"{BASE_URL}/chat/api/conversations/{conv_id}/messages/", json=ai_msg_data)
        print_response(response, "发送AI消息")
    
    # 获取对话历史
    response = requests.get(f"{BASE_URL}/chat/api/conversations/history/?search=API")
    print_response(response, "搜索对话历史")
    
    # 获取统计信息
    response = requests.get(f"{BASE_URL}/chat/api/conversations/statistics/")
    print_response(response, "获取对话统计")

def test_documents_apis():
    """测试Documents应用API"""
    print_section("2. Documents应用API测试")
    
    # 2.1 测试文档管理
    print("\n2.1 文档管理API")
    
    # 获取文档列表
    response = requests.get(f"{BASE_URL}/documents/api/documents/")
    print_response(response, "获取文档列表")
    
    # 创建新文档
    doc_data = {
        "title": "API测试文档",
        "content": "这是通过API创建的测试文档内容。包含一些示例文本用于测试搜索和处理功能。",
        "file_type": "txt",
        "metadata": {"source": "api_test", "created_by": "test_script"}
    }
    response = requests.post(f"{BASE_URL}/documents/api/documents/", json=doc_data)
    doc = print_response(response, "创建新文档")
    
    if doc and 'id' in doc:
        doc_id = doc['id']
        
        # 获取文档详情
        response = requests.get(f"{BASE_URL}/documents/api/documents/{doc_id}/")
        print_response(response, "获取文档详情")
        
        # 处理文档
        response = requests.post(f"{BASE_URL}/documents/api/documents/{doc_id}/process/")
        print_response(response, "处理文档")
        
        # 获取文档片段
        response = requests.get(f"{BASE_URL}/documents/api/documents/{doc_id}/chunks/")
        print_response(response, "获取文档片段")
    
    # 搜索文档
    response = requests.get(f"{BASE_URL}/documents/api/documents/search/?query=API")
    print_response(response, "搜索文档")
    
    # 获取文档统计
    response = requests.get(f"{BASE_URL}/documents/api/documents/statistics/")
    print_response(response, "获取文档统计")

def test_quiz_apis():
    """测试Quiz应用API"""
    print_section("3. Quiz应用API测试")
    
    # 3.1 测试测验管理
    print("\n3.1 测验管理API")
    
    # 获取测验列表
    response = requests.get(f"{BASE_URL}/quiz/api/quizzes/")
    print_response(response, "获取测验列表")
    
    # 创建新测验
    quiz_data = {
        "title": "API测试测验",
        "description": "通过API创建的测试测验",
        "difficulty_level": 2,
        "time_limit": 1800,
        "passing_score": 60,
        "metadata": {"created_by": "api_test"}
    }
    response = requests.post(f"{BASE_URL}/quiz/api/quizzes/", json=quiz_data)
    quiz = print_response(response, "创建新测验")
    
    if quiz and 'id' in quiz:
        quiz_id = quiz['id']
        
        # 获取测验详情
        response = requests.get(f"{BASE_URL}/quiz/api/quizzes/{quiz_id}/")
        print_response(response, "获取测验详情")
        
        # 创建测验问题
        question_data = {
            "quiz": quiz_id,
            "content": "Python是什么类型的编程语言？",
            "text": "Python是什么类型的编程语言？",
            "question_type": "MC",
            "options": ["解释型", "编译型", "混合型", "脚本型"],
            "correct_answer": ["解释型"],
            "explanation": "Python是一种解释型编程语言",
            "difficulty": 1,
            "points": 10
        }
        response = requests.post(f"{BASE_URL}/quiz/api/quizzes/{quiz_id}/questions/", json=question_data)
        print_response(response, "创建测验问题")
        
        # 获取测验问题列表
        response = requests.get(f"{BASE_URL}/quiz/api/quizzes/{quiz_id}/questions/")
        print_response(response, "获取测验问题")
        
        # 开始测验尝试
        attempt_data = {"quiz": quiz_id}
        response = requests.post(f"{BASE_URL}/quiz/api/quizzes/{quiz_id}/attempts/", json=attempt_data)
        attempt = print_response(response, "开始测验尝试")
        
        if attempt and 'id' in attempt:
            attempt_id = attempt['id']
            
            # 提交测验答案
            submit_data = {
                "answers": {
                    "1": ["解释型"]  # 假设问题ID为1
                }
            }
            response = requests.post(f"{BASE_URL}/quiz/api/attempts/{attempt_id}/submit/", json=submit_data)
            print_response(response, "提交测验答案")
        
        # 获取测验尝试列表
        response = requests.get(f"{BASE_URL}/quiz/api/quizzes/{quiz_id}/attempts/")
        print_response(response, "获取测验尝试列表")
    
    # 搜索测验
    response = requests.get(f"{BASE_URL}/quiz/api/quizzes/search/?query=API")
    print_response(response, "搜索测验")
    
    # 获取测验统计
    response = requests.get(f"{BASE_URL}/quiz/api/quizzes/statistics/")
    print_response(response, "获取测验统计")

def test_error_handling():
    """测试错误处理"""
    print_section("4. 错误处理测试")
    
    # 测试不存在的资源
    response = requests.get(f"{BASE_URL}/chat/api/conversations/99999/")
    print_response(response, "访问不存在的对话")
    
    response = requests.get(f"{BASE_URL}/documents/api/documents/99999/")
    print_response(response, "访问不存在的文档")
    
    response = requests.get(f"{BASE_URL}/quiz/api/quizzes/99999/")
    print_response(response, "访问不存在的测验")
    
    # 测试无效数据
    invalid_data = {"title": ""}  # 空标题
    response = requests.post(f"{BASE_URL}/chat/api/conversations/", json=invalid_data)
    print_response(response, "创建无效对话")

def main():
    """主测试函数"""
    print("🚀 问泉项目完整API测试")
    print("📅 测试时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("🔗 API基础URL:", BASE_URL)
    
    try:
        # 检查服务器连接
        response = requests.get(f"{BASE_URL}/chat/api/conversations/", timeout=5)
        if response.status_code != 200:
            print("❌ 无法连接到服务器，请确保Django服务器正在运行")
            return
        
        print("✅ 服务器连接正常")
        
        # 执行各项测试
        test_chat_apis()
        test_documents_apis()
        test_quiz_apis()
        test_error_handling()
        
        print_section("测试完成")
        print("🎉 所有API测试完成！")
        print("📊 测试涵盖了以下功能:")
        print("   ✓ Chat应用 - 对话和消息管理")
        print("   ✓ Documents应用 - 文档管理和处理")
        print("   ✓ Quiz应用 - 测验和问题管理")
        print("   ✓ 错误处理和边界情况")
        print("\n💡 您可以在浏览器中访问以下API浏览器:")
        print("   📖 Chat API: http://127.0.0.1:8000/chat/api/conversations/")
        print("   📖 Documents API: http://127.0.0.1:8000/documents/api/documents/")
        print("   📖 Quiz API: http://127.0.0.1:8000/quiz/api/quizzes/")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败：请确保Django服务器在 http://127.0.0.1:8000 运行")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == '__main__':
    main()
