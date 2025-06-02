# 问泉项目 API 结构设计

## 📋 概述

本文档详细说明了问泉项目按照Django最佳实践重新设计的API结构。新的API结构提供了更好的组织性、可维护性和扩展性。

## 🏗️ API架构设计

### 设计原则

1. **应用分离**: 每个Django应用管理自己的API端点
2. **版本控制**: 使用版本化路径支持API演进
3. **向后兼容**: 保持旧版API路径的兼容性
4. **RESTful设计**: 遵循REST API设计规范
5. **统一入口**: 提供API根视图和健康检查

### 目录结构

```
问泉项目 API 结构
├── /api/                           # 主API根路径
│   ├── /                          # API概览和导航
│   ├── /health/                   # 健康检查
│   └── /v1/                       # API版本1
│       ├── /chat/                 # Chat应用API
│       ├── /documents/            # Documents应用API
│       └── /quiz/                 # Quiz应用API
├── /chat/                         # Chat应用 (兼容性)
├── /documents/                    # Documents应用 (兼容性)
└── /quiz/                         # Quiz应用 (兼容性)
```

## 🔗 API端点映射

### 主API端点

| 端点 | 方法 | 描述 | 视图函数 |
|------|------|------|----------|
| `/api/` | GET | API根视图，提供概览 | `api_views.api_root` |
| `/api/health/` | GET | API健康检查 | `api_views.api_health` |

### Chat应用API

#### 版本化API (推荐)
| 端点 | 方法 | 描述 | 视图类/函数 |
|------|------|------|-------------|
| `/api/v1/chat/` | GET | Chat API根视图 | `chat.views.chat_api_root` |
| `/api/v1/chat/conversations/` | GET, POST | 对话列表/创建 | `ConversationListAPIView` |
| `/api/v1/chat/conversations/{id}/` | GET, PUT, DELETE | 对话详情 | `ConversationDetailAPIView` |
| `/api/v1/chat/conversations/history/` | GET | 对话历史 | `conversation_history_api_view` |
| `/api/v1/chat/conversations/statistics/` | GET | 对话统计 | `conversation_statistics_api_view` |
| `/api/v1/chat/conversations/{id}/messages/` | GET, POST | 消息列表/创建 | `MessageListAPIView` |
| `/api/v1/chat/messages/{id}/` | GET, PUT, DELETE | 消息详情 | `MessageDetailAPIView` |
| `/api/v1/chat/messages/{id}/feedback/` | POST | 消息反馈 | `message_feedback_api_view` |

#### 兼容性API
| 端点 | 方法 | 描述 |
|------|------|------|
| `/chat/` | GET | Chat应用根视图 |
| `/chat/api/conversations/` | GET, POST | 对话列表/创建 (兼容) |
| `/chat/api/conversations/{id}/` | GET, PUT, DELETE | 对话详情 (兼容) |
| ... | ... | 其他端点保持兼容 |

### Documents应用API

#### 版本化API (推荐)
| 端点 | 方法 | 描述 | 视图类/函数 |
|------|------|------|-------------|
| `/api/v1/documents/` | GET | Documents API根视图 | `documents.views.documents_api_root` |
| `/api/v1/documents/documents/` | GET, POST | 文档列表/创建 | `DocumentListAPIView` |
| `/api/v1/documents/documents/{id}/` | GET, PUT, DELETE | 文档详情 | `DocumentDetailAPIView` |
| `/api/v1/documents/documents/search/` | GET | 文档搜索 | `document_search_api_view` |
| `/api/v1/documents/documents/statistics/` | GET | 文档统计 | `document_statistics_api_view` |
| `/api/v1/documents/documents/{id}/process/` | POST | 文档处理 | `document_process_api_view` |
| `/api/v1/documents/documents/{id}/chunks/` | GET, POST | 文档分块 | `DocumentChunkListAPIView` |

#### 兼容性API
| 端点 | 方法 | 描述 |
|------|------|------|
| `/documents/` | GET | Documents应用根视图 |
| `/documents/api/documents/` | GET, POST | 文档列表/创建 (兼容) |
| `/documents/api/documents/{id}/` | GET, PUT, DELETE | 文档详情 (兼容) |
| ... | ... | 其他端点保持兼容 |

### Quiz应用API

#### 版本化API (推荐)
| 端点 | 方法 | 描述 | 视图类/函数 |
|------|------|------|-------------|
| `/api/v1/quiz/` | GET | Quiz API根视图 | `quiz.views.quiz_api_root` |
| `/api/v1/quiz/quizzes/` | GET, POST | 测验列表/创建 | `QuizListAPIView` |
| `/api/v1/quiz/quizzes/{id}/` | GET, PUT, DELETE | 测验详情 | `QuizDetailAPIView` |
| `/api/v1/quiz/quizzes/search/` | GET | 测验搜索 | `quiz_search_api_view` |
| `/api/v1/quiz/quizzes/statistics/` | GET | 测验统计 | `quiz_statistics_api_view` |
| `/api/v1/quiz/quizzes/{id}/questions/` | GET, POST | 问题列表/创建 | `QuestionListAPIView` |
| `/api/v1/quiz/quizzes/{id}/attempts/` | GET, POST | 测验尝试 | `QuizAttemptListAPIView` |
| `/api/v1/quiz/attempts/` | GET | 所有尝试 | `QuizAttemptListAPIView` |
| `/api/v1/quiz/attempts/{id}/submit/` | POST | 提交答案 | `quiz_attempt_submit_api_view` |

#### 兼容性API
| 端点 | 方法 | 描述 |
|------|------|------|
| `/quiz/` | GET | Quiz应用根视图 |
| `/quiz/api/quizzes/` | GET, POST | 测验列表/创建 (兼容) |
| `/quiz/api/quizzes/{id}/` | GET, PUT, DELETE | 测验详情 (兼容) |
| ... | ... | 其他端点保持兼容 |

## 📁 文件组织

### URL配置文件

```
InquirySpring/
├── urls.py                        # 主URL配置
├── api_views.py                   # 主API视图
└── apps/
    ├── chat/
    │   ├── urls.py               # Chat应用URL配置
    │   └── views.py              # Chat应用视图
    ├── documents/
    │   ├── urls.py               # Documents应用URL配置
    │   └── views.py              # Documents应用视图
    └── quiz/
        ├── urls.py               # Quiz应用URL配置
        └── views.py              # Quiz应用视图
```

### 主URL配置 (InquirySpring/urls.py)

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 主API根视图
    path('api/', api_views.api_root, name='api_root'),
    path('api/health/', api_views.api_health, name='api_health'),

    # API v1 路由
    path('api/v1/chat/', include('apps.chat.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),
    path('api/v1/quiz/', include('apps.quiz.urls')),
    
    # 兼容性路由
    path('chat/', include('apps.chat.urls')),
    path('documents/', include('apps.documents.urls')),
    path('quiz/', include('apps.quiz.urls')),
]
```

### 应用URL配置示例 (apps/chat/urls.py)

```python
urlpatterns = [
    # API根视图
    path('', views.chat_api_root, name='api_root'),
    
    # 对话管理API
    path('conversations/', views.ConversationListAPIView.as_view(), name='conversation_list'),
    path('conversations/<int:pk>/', views.ConversationDetailAPIView.as_view(), name='conversation_detail'),
    # ... 其他端点
    
    # 兼容性路由
    path('api/conversations/', views.ConversationListAPIView.as_view(), name='api_conversation_list'),
    # ... 其他兼容性端点
]
```

## 🔄 迁移指南

### 对于前端开发者

#### 推荐做法
1. **使用版本化API**: 优先使用 `/api/v1/` 路径
2. **API根视图**: 从 `/api/v1/{app}/` 获取端点概览
3. **健康检查**: 使用 `/api/health/` 检查服务状态

#### 迁移步骤
1. 将现有API调用从 `/{app}/api/` 更新为 `/api/v1/{app}/`
2. 更新API基础URL配置
3. 测试新端点的功能
4. 逐步移除对旧端点的依赖

#### 示例迁移

```javascript
// 旧版API调用
const oldUrl = 'http://127.0.0.1:8000/chat/api/conversations/';

// 新版API调用 (推荐)
const newUrl = 'http://127.0.0.1:8000/api/v1/chat/conversations/';

// 兼容性调用 (仍然可用)
const compatUrl = 'http://127.0.0.1:8000/chat/api/conversations/';
```

### 对于后端开发者

#### 添加新端点
1. 在相应应用的 `views.py` 中添加视图
2. 在应用的 `urls.py` 中添加路由
3. 同时添加版本化路径和兼容性路径
4. 更新API根视图中的端点列表

#### 版本管理
1. 新功能优先在版本化API中实现
2. 保持兼容性API的稳定性
3. 计划未来版本的API变更

## 🧪 测试

### 自动化测试

```bash
# 测试新API结构
python test_new_api_structure.py

# 测试所有API功能
python test_all_apis.py
```

### 手动测试

1. **API根视图**: http://127.0.0.1:8000/api/
2. **健康检查**: http://127.0.0.1:8000/api/health/
3. **应用API**: http://127.0.0.1:8000/api/v1/{app}/

## 📈 优势

### 1. 更好的组织性
- 清晰的应用边界
- 统一的API入口
- 版本化管理

### 2. 向后兼容性
- 旧版API继续可用
- 平滑的迁移路径
- 减少破坏性变更

### 3. 可扩展性
- 支持API版本演进
- 易于添加新功能
- 模块化设计

### 4. 开发体验
- API浏览器支持
- 自动化测试
- 详细的文档

## 🔮 未来规划

### API v2 规划
- 改进的数据结构
- 更好的性能优化
- 新的功能特性

### 兼容性策略
- 维护v1 API的稳定性
- 提供迁移工具和文档
- 逐步弃用旧版端点

---

**问泉项目 - 构建可扩展的API架构！** 🚀
