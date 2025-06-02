# 问泉项目前端API对接指南

## 📋 概述

本文档为前端团队提供完整的API对接指南。后端团队已完成所有API设计和数据库管理，前端团队可以直接使用这些API进行开发。

## 🔗 API基础信息

### 服务器地址
- **开发环境**: http://127.0.0.1:7890
- **API根路径**: http://127.0.0.1:8000/api/
- **API版本**: v1 (推荐使用版本化路径)

### API路径结构
- **版本化API** (推荐): `/api/v1/{app}/`
- **兼容性API**: `/{app}/api/` (保持向后兼容)
- **应用根视图**: `/api/v1/{app}/` (提供API概览)

### 数据格式
- **请求格式**: JSON
- **响应格式**: JSON
- **字符编码**: UTF-8
- **时间格式**: ISO 8601 (例: "2025-06-02T12:59:41.683825Z")

### HTTP状态码
- **200**: 成功
- **201**: 创建成功
- **400**: 请求参数错误
- **404**: 资源不存在
- **500**: 服务器内部错误

## 📱 Chat应用API

### 推荐路径: `/api/v1/chat/`
### 兼容路径: `/chat/api/` (向后兼容)

#### 1. 对话管理

**API根视图**
```
GET /api/v1/chat/
响应: API概览和端点列表
```

**获取对话列表**
```
GET /api/v1/chat/conversations/
参数:
  - page: 页码 (可选)
  - page_size: 每页数量 (可选, 默认20)
  - search: 搜索关键词 (可选)
  - mode: 对话模式 (可选: chat, summary, quiz)

响应示例:
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "测试对话",
      "mode": "chat",
      "user": null,
      "document": null,
      "message_count": 5,
      "last_message": {
        "content": "最后一条消息",
        "is_user": true,
        "created_at": "2025-06-02T12:59:41Z"
      },
      "is_active": true,
      "created_at": "2025-06-02T11:34:37Z",
      "updated_at": "2025-06-02T11:34:37Z"
    }
  ]
}
```

**创建新对话**
```
POST /api/v1/chat/conversations/
请求体:
{
  "title": "对话标题",
  "mode": "chat",
  "document": null,
  "context": "对话上下文"
}

响应: 201 Created
{
  "id": 1,
  "title": "对话标题",
  "mode": "chat",
  "document": null,
  "context": "对话上下文"
}
```

**获取对话详情**
```
GET /chat/api/conversations/{id}/
响应: 对话详细信息，包含所有消息
```

#### 2. 消息管理

**获取对话消息**
```
GET /chat/api/conversations/{conversation_id}/messages/
参数:
  - page: 页码
  - page_size: 每页数量

响应: 消息列表
```

**发送消息**
```
POST /chat/api/conversations/{conversation_id}/messages/
请求体:
{
  "content": "消息内容",
  "is_user": true
}

响应: 201 Created
```

#### 3. 统计和搜索

**对话统计**
```
GET /chat/api/conversations/statistics/
响应: 对话和消息统计数据
```

**对话历史搜索**
```
GET /chat/api/conversations/history/
参数:
  - search: 搜索关键词
  - start_date: 开始日期
  - end_date: 结束日期
```

## 📄 Documents应用API

### 推荐路径: `/api/v1/documents/`
### 兼容路径: `/documents/api/` (向后兼容)

#### 1. 文档管理

**API根视图**
```
GET /api/v1/documents/
响应: API概览和端点列表
```

**获取文档列表**
```
GET /api/v1/documents/documents/
参数:
  - page: 页码
  - page_size: 每页数量
  - file_type: 文件类型过滤
  - is_processed: 是否已处理

响应示例:
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "title": "文档标题",
      "file_type": "txt",
      "file_size": 105,
      "chunk_count": 0,
      "conversation_count": 0,
      "is_processed": false,
      "created_at": "2025-06-02T12:07:10Z",
      "updated_at": "2025-06-02T12:07:10Z"
    }
  ]
}
```

**创建文档**
```
POST /documents/api/documents/
请求体:
{
  "title": "文档标题",
  "content": "文档内容",
  "file_type": "txt",
  "metadata": {
    "source": "upload",
    "tags": ["tag1", "tag2"]
  }
}
```

**获取文档详情**
```
GET /documents/api/documents/{id}/
响应: 完整文档信息，包含内容和分块
```

#### 2. 文档搜索和处理

**搜索文档**
```
GET /documents/api/documents/search/
参数:
  - query: 搜索关键词
  - file_type: 文件类型
  - start_date: 开始日期
  - end_date: 结束日期

响应: 匹配的文档列表
```

**处理文档**
```
POST /documents/api/documents/{id}/process/
请求体:
{
  "chunk_size": 1000,
  "overlap": 100
}

响应: 处理结果
```

**文档统计**
```
GET /documents/api/documents/statistics/
响应: 文档统计信息
```

## 🧩 Quiz应用API

### 推荐路径: `/api/v1/quiz/`
### 兼容路径: `/quiz/api/` (向后兼容)

#### 1. 测验管理

**API根视图**
```
GET /api/v1/quiz/
响应: API概览和端点列表
```

**获取测验列表**
```
GET /api/v1/quiz/quizzes/
参数:
  - page: 页码
  - difficulty_level: 难度级别 (1-4)
  - document_id: 关联文档ID
  - is_active: 是否激活

响应示例:
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "title": "测验标题",
      "description": "测验描述",
      "user": null,
      "document": null,
      "question_count": 5,
      "attempt_count": 0,
      "average_score": 0,
      "difficulty_level": 2,
      "time_limit": 1800,
      "is_active": true,
      "created_at": "2025-06-02T12:19:46Z"
    }
  ]
}
```

**创建测验**
```
POST /quiz/api/quizzes/
请求体:
{
  "title": "测验标题",
  "description": "测验描述",
  "document": null,
  "difficulty_level": 2,
  "time_limit": 1800,
  "passing_score": 60,
  "metadata": {
    "created_by": "user"
  }
}
```

#### 2. 问题管理

**获取测验问题**
```
GET /quiz/api/quizzes/{quiz_id}/questions/
响应: 测验的所有问题
```

**创建问题**
```
POST /quiz/api/quizzes/{quiz_id}/questions/
请求体:
{
  "content": "问题内容",
  "question_type": "MC",
  "options": ["选项A", "选项B", "选项C", "选项D"],
  "correct_answer": "选项A",
  "explanation": "答案解释"
}
```

#### 3. 测验尝试

**开始测验**
```
POST /quiz/api/quizzes/{quiz_id}/attempts/
请求体:
{
  "metadata": {
    "start_reason": "practice"
  }
}

响应: 测验尝试记录
```

**提交答案**
```
POST /quiz/api/attempts/{attempt_id}/submit/
请求体:
{
  "answers": {
    "1": "选项A",
    "2": "选项B"
  }
}

响应: 评分结果和详细反馈
```

#### 4. 搜索和统计

**搜索测验**
```
GET /quiz/api/quizzes/search/
参数:
  - query: 搜索关键词
  - difficulty_level: 难度级别
  - start_date: 开始日期
  - end_date: 结束日期
```

**测验统计**
```
GET /quiz/api/quizzes/statistics/
响应: 测验统计数据
```

## 🔐 认证和权限

### 当前状态
- 所有API端点当前设置为 `AllowAny`，便于开发测试
- 支持用户认证机制，可以根据需要启用

### 用户认证 (可选)
```javascript
// 如果启用认证，在请求头中添加:
headers: {
  'Authorization': 'Token your-auth-token',
  'Content-Type': 'application/json'
}
```

## 📝 前端开发建议

### 1. API调用示例 (JavaScript)

```javascript
// 获取对话列表 (推荐使用版本化API)
async function getConversations() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/chat/conversations/');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('获取对话列表失败:', error);
  }
}

// 创建新对话
async function createConversation(title, mode = 'chat') {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/chat/conversations/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: title,
        mode: mode,
        context: '通过前端创建的对话'
      })
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('创建对话失败:', error);
  }
}

// 发送消息
async function sendMessage(conversationId, content) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/chat/conversations/${conversationId}/messages/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: content,
        is_user: true
      })
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('发送消息失败:', error);
  }
}
```

### 2. 错误处理

```javascript
async function handleApiCall(url, options = {}) {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`API错误 ${response.status}: ${JSON.stringify(errorData)}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API调用失败:', error);
    // 显示用户友好的错误消息
    showErrorMessage('操作失败，请稍后重试');
    throw error;
  }
}
```

### 3. 分页处理

```javascript
async function loadMoreData(nextUrl) {
  if (!nextUrl) return null;
  
  const response = await fetch(nextUrl);
  return await response.json();
}
```

## 🧪 测试和调试

### API浏览器
- **主API概览**: http://127.0.0.1:8000/api/
- **Chat API**: http://127.0.0.1:8000/api/v1/chat/
- **Documents API**: http://127.0.0.1:8000/api/v1/documents/
- **Quiz API**: http://127.0.0.1:8000/api/v1/quiz/

### 兼容性API浏览器 (旧版)
- **Chat API**: http://127.0.0.1:8000/chat/api/conversations/
- **Documents API**: http://127.0.0.1:8000/documents/api/documents/
- **Quiz API**: http://127.0.0.1:8000/quiz/api/quizzes/

### 测试脚本
```bash
# 运行完整API测试
python test_all_apis.py
```

### 调试建议
1. 使用浏览器开发者工具查看网络请求
2. 检查请求头和响应状态码
3. 验证JSON格式的正确性
4. 使用API浏览器进行手动测试

## 📞 技术支持

如有API相关问题，请联系后端团队：
- 检查API文档和示例
- 运行测试脚本验证API状态
- 查看Django服务器日志获取详细错误信息

---

**祝前端开发顺利！** 🚀
