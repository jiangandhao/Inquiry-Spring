# 问泉 (Inquiry Spring) - API设计与数据库管理

## 🎯 项目定位

**专注于API设计和数据库管理的后端项目**

问泉是一个基于Django的智能对话历史管理系统后端，为前端团队提供完整的RESTful API接口。本项目专注于：
- ✅ 完整的API设计
- ✅ 高效的数据库管理
- ✅ 标准化的数据处理
- 🚫 前端开发由其他团队负责

## 🏗️ 系统架构

### 核心应用模块

#### 1. Chat应用 (对话管理)
- 多模式对话支持（聊天、总结、测验）
- 对话历史记录和搜索
- 消息管理和反馈系统
- 实时对话统计分析

#### 2. Documents应用 (文档管理)
- 文档存储和元数据管理
- 文档内容分析和分块处理
- 智能文档搜索功能
- 文档处理状态跟踪

#### 3. Quiz应用 (测验系统)
- 测验创建和管理
- 多种题型支持
- 测验尝试和评分
- 统计分析和报告

## 🛠️ 技术栈

- **后端框架**: Django 5.2
- **API框架**: Django REST Framework
- **数据库**: SQLite (开发) / PostgreSQL (生产推荐)
- **Python版本**: 3.8+
- **API设计**: RESTful架构
- **数据格式**: JSON

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd Inquiry-Spring

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库设置

```bash
# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 3. 启动API服务

```bash
# 启动开发服务器
python manage.py runserver

# API服务地址: http://127.0.0.1:8000
# Django管理后台: http://127.0.0.1:8000/admin/
```

### 4. API测试

```bash
# 运行完整API测试
python test_all_apis.py
```

## 📡 API接口总览

### 主API端点
```
GET    /api/                                       # API根视图和概览
GET    /api/health/                                # API健康检查
```

### Chat API (对话管理) - 推荐使用版本化路径
```
GET    /api/v1/chat/                               # Chat API根视图
GET    /api/v1/chat/conversations/                 # 对话列表
POST   /api/v1/chat/conversations/                 # 创建对话
GET    /api/v1/chat/conversations/{id}/            # 对话详情
GET    /api/v1/chat/conversations/history/         # 对话历史
GET    /api/v1/chat/conversations/statistics/      # 对话统计
GET    /api/v1/chat/conversations/{id}/messages/   # 消息列表
POST   /api/v1/chat/conversations/{id}/messages/   # 发送消息
POST   /api/v1/chat/messages/{id}/feedback/        # 消息反馈
```

### Documents API (文档管理) - 推荐使用版本化路径
```
GET    /api/v1/documents/                          # Documents API根视图
GET    /api/v1/documents/documents/                # 文档列表
POST   /api/v1/documents/documents/                # 创建文档
GET    /api/v1/documents/documents/{id}/           # 文档详情
GET    /api/v1/documents/documents/search/         # 搜索文档
GET    /api/v1/documents/documents/statistics/     # 文档统计
POST   /api/v1/documents/documents/{id}/process/   # 处理文档
GET    /api/v1/documents/documents/{id}/chunks/    # 文档分块
```

### Quiz API (测验系统) - 推荐使用版本化路径
```
GET    /api/v1/quiz/                               # Quiz API根视图
GET    /api/v1/quiz/quizzes/                       # 测验列表
POST   /api/v1/quiz/quizzes/                       # 创建测验
GET    /api/v1/quiz/quizzes/{id}/                  # 测验详情
GET    /api/v1/quiz/quizzes/search/                # 搜索测验
GET    /api/v1/quiz/quizzes/statistics/            # 测验统计
GET    /api/v1/quiz/quizzes/{id}/questions/        # 问题列表
POST   /api/v1/quiz/quizzes/{id}/attempts/         # 开始测验
POST   /api/v1/quiz/attempts/{id}/submit/          # 提交答案
```

### 兼容性API (向后兼容)
```
# 旧版API路径仍然可用，但建议使用版本化路径
/chat/api/conversations/                          # Chat兼容API
/documents/api/documents/                         # Documents兼容API
/quiz/api/quizzes/                                # Quiz兼容API
```

## 🔍 API浏览器

Django REST Framework提供的可视化API浏览器：

### 推荐的版本化API浏览器
- **主API概览**: http://127.0.0.1:8000/api/
- **API健康检查**: http://127.0.0.1:8000/api/health/
- **Chat API**: http://127.0.0.1:8000/api/v1/chat/
- **Documents API**: http://127.0.0.1:8000/api/v1/documents/
- **Quiz API**: http://127.0.0.1:8000/api/v1/quiz/

### 兼容性API浏览器 (旧版)
- **Chat API**: http://127.0.0.1:8000/chat/api/conversations/
- **Documents API**: http://127.0.0.1:8000/documents/api/documents/
- **Quiz API**: http://127.0.0.1:8000/quiz/api/quizzes/

## 📊 数据库设计

### 核心数据模型

#### Chat应用
- **Conversation**: 对话记录
- **Message**: 消息内容

#### Documents应用
- **Document**: 文档信息
- **DocumentChunk**: 文档分块

#### Quiz应用
- **Quiz**: 测验信息
- **Question**: 问题内容
- **QuizAttempt**: 测验尝试

### 数据库管理

```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 查看迁移状态
python manage.py showmigrations

# 重置数据库（开发环境）
python manage.py flush
```

## 📋 前端团队对接

### API文档
- **详细API文档**: `API_DOCUMENTATION.md`
- **前端对接指南**: `FRONTEND_API_GUIDE.md`
- **项目总结**: `API_SUMMARY.md`

### 关键特性
- ✅ **标准化接口**: 遵循RESTful设计原则
- ✅ **JSON格式**: 统一的数据交换格式
- ✅ **分页支持**: 所有列表接口支持分页
- ✅ **搜索功能**: 完善的搜索和过滤
- ✅ **错误处理**: 统一的错误响应格式
- ✅ **性能优化**: 数据库查询优化

### 认证机制
- 当前设置为 `AllowAny` 便于开发
- 支持Token认证，可根据需要启用
- 完善的权限控制系统

## 🧪 测试和质量保证

### 自动化测试
```bash
# 运行Django单元测试
python manage.py test

# 运行API集成测试
python test_all_apis.py

# 测试特定应用
python manage.py test apps.chat
```

### 代码质量
- 完整的API测试覆盖
- 标准化的错误处理
- 详细的代码注释
- 规范的命名约定

## 📈 性能优化

### 数据库优化
- 合理的索引设计
- 查询优化（select_related, prefetch_related）
- 分页查询避免大量数据加载

### API优化
- 序列化器字段控制
- 缓存策略支持
- 压缩响应数据

## 🔧 开发和维护

### 添加新API
1. 在相应应用中创建模型
2. 编写序列化器
3. 创建API视图
4. 配置URL路由
5. 编写测试用例
6. 更新API文档

### 数据库变更
1. 修改模型定义
2. 创建迁移文件
3. 测试迁移
4. 应用到生产环境

## 🚀 部署建议

### 生产环境
- 使用PostgreSQL数据库
- 配置Redis缓存
- 设置Nginx + Gunicorn
- 启用HTTPS
- 配置日志系统

### 环境变量
```bash
# 数据库配置
DATABASE_URL=postgresql://user:pass@localhost/dbname

# 安全配置
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# 缓存配置
REDIS_URL=redis://localhost:6379/0
```

## 📞 技术支持

### 文档资源
- `API_DOCUMENTATION.md` - 完整API文档
- `FRONTEND_API_GUIDE.md` - 前端对接指南
- `API_SUMMARY.md` - 项目总结

### 联系方式
- 项目Issues: GitHub Issues
- 技术讨论: 团队内部沟通渠道

---

**问泉项目 - 为智能对话系统提供强大的API支撑！** 🌟
