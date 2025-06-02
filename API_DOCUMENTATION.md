# 问泉项目 API 文档

## 概述

问泉项目提供了完整的REST API接口，涵盖对话管理、文档处理和测验系统三大核心功能模块。所有API都支持JSON格式的数据交换，并提供了完善的错误处理和分页功能。

## 基础信息

- **基础URL**: `http://127.0.0.1:8000`
- **数据格式**: JSON
- **认证方式**: 可选用户认证（支持匿名访问）
- **分页**: 支持标准分页，默认每页20条记录

## 1. 对话管理 API (Chat)

### 1.1 对话相关接口

#### 获取对话列表
```
GET /chat/api/conversations/
```
**查询参数**:
- `page_size`: 每页数量（默认20）
- `search`: 搜索关键词
- `mode`: 对话模式过滤
- `is_active`: 是否激活

**响应示例**:
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/chat/api/conversations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Python学习讨论",
      "mode": "chat",
      "user": null,
      "document": null,
      "message_count": 5,
      "last_message": "最后一条消息内容",
      "is_active": true,
      "created_at": "2025-06-02T10:00:00Z",
      "updated_at": "2025-06-02T11:00:00Z"
    }
  ]
}
```

#### 创建新对话
```
POST /chat/api/conversations/
```
**请求体**:
```json
{
  "title": "新对话标题",
  "mode": "chat",
  "context": "对话上下文"
}
```

#### 获取对话详情
```
GET /chat/api/conversations/{id}/
```
**响应包含**: 对话基本信息 + 所有消息列表

#### 获取对话历史（支持搜索）
```
GET /chat/api/conversations/history/
```
**查询参数**:
- `search`: 搜索关键词
- `page_size`: 每页数量
- `mode`: 对话模式

#### 获取对话统计信息
```
GET /chat/api/conversations/statistics/
```
**响应示例**:
```json
{
  "success": true,
  "data": {
    "total_conversations": 25,
    "active_conversations": 20,
    "mode_statistics": {
      "chat": 15,
      "summary": 5,
      "quiz": 5
    },
    "message_statistics": {
      "total_messages": 150,
      "user_messages": 75,
      "ai_messages": 75
    },
    "recent_conversations": [...]
  }
}
```

### 1.2 消息相关接口

#### 获取对话消息列表
```
GET /chat/api/conversations/{conversation_id}/messages/
```

#### 发送新消息
```
POST /chat/api/conversations/{conversation_id}/messages/
```
**请求体**:
```json
{
  "content": "消息内容",
  "is_user": true,
  "metadata": {"timestamp": "2025-06-02T10:00:00Z"}
}
```

#### 获取消息详情
```
GET /chat/api/messages/{id}/
```

#### 提交消息反馈
```
POST /chat/api/messages/{message_id}/feedback/
```
**请求体**:
```json
{
  "feedback_score": 5,
  "feedback_comment": "很有帮助的回答"
}
```

## 2. 文档管理 API (Documents)

### 2.1 文档相关接口

#### 获取文档列表
```
GET /documents/api/documents/
```
**查询参数**:
- `search`: 搜索关键词
- `file_type`: 文件类型
- `is_processed`: 是否已处理

#### 创建新文档
```
POST /documents/api/documents/
```
**请求体**:
```json
{
  "title": "文档标题",
  "content": "文档内容",
  "file_type": "txt",
  "metadata": {"source": "upload"}
}
```

#### 获取文档详情
```
GET /documents/api/documents/{id}/
```

#### 文档搜索
```
GET /documents/api/documents/search/
```
**查询参数**:
- `query`: 搜索关键词
- `file_type`: 文件类型
- `start_date`: 开始时间
- `end_date`: 结束时间
- `min_size`: 最小文件大小
- `max_size`: 最大文件大小

#### 文档统计信息
```
GET /documents/api/documents/statistics/
```

#### 处理文档
```
POST /documents/api/documents/{document_id}/process/
```

### 2.2 文档片段接口

#### 获取文档片段列表
```
GET /documents/api/documents/{document_id}/chunks/
```

#### 创建文档片段
```
POST /documents/api/documents/{document_id}/chunks/
```

## 3. 测验系统 API (Quiz)

### 3.1 测验相关接口

#### 获取测验列表
```
GET /quiz/api/quizzes/
```
**查询参数**:
- `search`: 搜索关键词
- `difficulty_level`: 难度级别
- `document_id`: 关联文档ID
- `is_active`: 是否激活

#### 创建新测验
```
POST /quiz/api/quizzes/
```
**请求体**:
```json
{
  "title": "Python基础测验",
  "description": "测验描述",
  "difficulty_level": 2,
  "time_limit": 1800,
  "passing_score": 60
}
```

#### 获取测验详情
```
GET /quiz/api/quizzes/{id}/
```

#### 测验搜索
```
GET /quiz/api/quizzes/search/
```

#### 测验统计信息
```
GET /quiz/api/quizzes/statistics/
```

### 3.2 问题相关接口

#### 获取测验问题列表
```
GET /quiz/api/quizzes/{quiz_id}/questions/
```

#### 创建新问题
```
POST /quiz/api/quizzes/{quiz_id}/questions/
```
**请求体**:
```json
{
  "quiz": 1,
  "text": "Python是什么类型的编程语言？",
  "question_type": "MC",
  "difficulty": 1,
  "points": 10,
  "explanation": "Python是一种解释型编程语言",
  "answers": [
    {
      "text": "解释型",
      "is_correct": true,
      "explanation": "正确答案"
    },
    {
      "text": "编译型",
      "is_correct": false,
      "explanation": "错误答案"
    }
  ]
}
```

### 3.3 测验尝试接口

#### 获取测验尝试列表
```
GET /quiz/api/quizzes/{quiz_id}/attempts/
GET /quiz/api/attempts/
```

#### 开始新的测验尝试
```
POST /quiz/api/quizzes/{quiz_id}/attempts/
```
**请求体**:
```json
{
  "quiz": 1
}
```

#### 提交测验答案
```
POST /quiz/api/attempts/{attempt_id}/submit/
```
**请求体**:
```json
{
  "answers": {
    "1": [1, 3],  // 问题ID: [答案ID列表]
    "2": [4],
    "3": [7, 8]
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "attempt_id": 1,
  "score": 80,
  "correct_answers": 4,
  "total_questions": 5,
  "accuracy": 80.0,
  "time_taken": 1200,
  "results": [
    {
      "question_id": 1,
      "question_text": "问题内容",
      "user_answers": [1],
      "correct_answers": [1],
      "is_correct": true,
      "points": 10,
      "explanation": "解释说明"
    }
  ]
}
```

## 4. 通用响应格式

### 成功响应
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}
```

### 错误响应
```json
{
  "success": false,
  "error": "错误信息",
  "errors": {
    "field_name": ["字段错误信息"]
  }
}
```

### 分页响应
```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/endpoint/?page=3",
  "previous": "http://127.0.0.1:8000/api/endpoint/?page=1",
  "results": [...]
}
```

## 5. 状态码说明

- `200 OK`: 请求成功
- `201 Created`: 资源创建成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未授权
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误

## 6. 使用示例

### Python 示例
```python
import requests

# 创建对话
response = requests.post(
    'http://127.0.0.1:8000/chat/api/conversations/',
    json={
        'title': 'API测试对话',
        'mode': 'chat',
        'context': '通过API创建的对话'
    }
)

# 发送消息
if response.status_code == 201:
    conversation_id = response.json()['id']
    requests.post(
        f'http://127.0.0.1:8000/chat/api/conversations/{conversation_id}/messages/',
        json={
            'content': '你好，这是通过API发送的消息',
            'is_user': True
        }
    )
```

### JavaScript 示例
```javascript
// 获取对话列表
fetch('http://127.0.0.1:8000/chat/api/conversations/')
  .then(response => response.json())
  .then(data => {
    console.log('对话列表:', data.results);
  });

// 创建新对话
fetch('http://127.0.0.1:8000/chat/api/conversations/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: '新对话',
    mode: 'chat',
    context: 'JavaScript创建的对话'
  })
})
.then(response => response.json())
.then(data => {
  console.log('创建成功:', data);
});
```

## 7. API浏览器

访问 `http://127.0.0.1:8000/chat/api/conversations/` 可以使用Django REST Framework提供的API浏览器界面，支持：
- 可视化API文档
- 在线测试API接口
- 查看请求/响应格式
- 交互式操作界面

---

**问泉项目** - 完整的对话历史管理、文档处理和测验系统API 🚀
