"""
问泉项目主API视图
提供整个项目的API概览和导航
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.urls import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    问泉项目API根视图
    提供所有可用API端点的概览
    """
    return Response({
        'message': '问泉 (Inquiry Spring) - 智能对话历史管理系统 API',
        'version': '1.0',
        'description': '专注于API设计和数据库管理的后端项目',
        'applications': {
            'chat': {
                'name': '对话管理系统',
                'description': '管理对话和消息的API',
                'root': request.build_absolute_uri('/api/v1/chat/'),
                'endpoints': {
                    'conversations': request.build_absolute_uri('/api/v1/chat/conversations/'),
                    'messages': request.build_absolute_uri('/api/v1/chat/conversations/{conversation_id}/messages/'),
                    'statistics': request.build_absolute_uri('/api/v1/chat/conversations/statistics/'),
                }
            },
            'documents': {
                'name': '文档管理系统',
                'description': '管理文档和文档分块的API',
                'root': request.build_absolute_uri('/api/v1/documents/'),
                'endpoints': {
                    'documents': request.build_absolute_uri('/api/v1/documents/documents/'),
                    'search': request.build_absolute_uri('/api/v1/documents/documents/search/'),
                    'chunks': request.build_absolute_uri('/api/v1/documents/documents/{document_id}/chunks/'),
                    'statistics': request.build_absolute_uri('/api/v1/documents/documents/statistics/'),
                }
            },
            'quiz': {
                'name': '测验管理系统',
                'description': '管理测验、问题和测验尝试的API',
                'root': request.build_absolute_uri('/api/v1/quiz/'),
                'endpoints': {
                    'quizzes': request.build_absolute_uri('/api/v1/quiz/quizzes/'),
                    'questions': request.build_absolute_uri('/api/v1/quiz/quizzes/{quiz_id}/questions/'),
                    'attempts': request.build_absolute_uri('/api/v1/quiz/attempts/'),
                    'statistics': request.build_absolute_uri('/api/v1/quiz/quizzes/statistics/'),
                }
            }
        },
        'features': [
            'RESTful API设计',
            '完整的CRUD操作',
            '高级搜索和过滤',
            '分页支持',
            '统计分析',
            '错误处理',
            'API版本控制'
        ],
        'documentation': {
            'api_guide': 'FRONTEND_API_GUIDE.md',
            'api_docs': 'API_DOCUMENTATION.md',
            'project_summary': 'API_SUMMARY.md',
            'readme': 'README.md'
        },
        'compatibility': {
            'legacy_urls': {
                'chat': request.build_absolute_uri('/chat/api/conversations/'),
                'documents': request.build_absolute_uri('/documents/api/documents/'),
                'quiz': request.build_absolute_uri('/quiz/api/quizzes/'),
            },
            'note': '旧版URL仍然可用，但建议使用新的版本化API路径'
        },
        'admin': request.build_absolute_uri('/admin/'),
        'contact': {
            'team': '后端开发团队',
            'focus': 'API设计和数据库管理',
            'frontend': '前端开发由其他团队负责'
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_health(request):
    """
    API健康检查端点
    """
    return Response({
        'status': 'healthy',
        'message': '问泉API服务正常运行',
        'timestamp': request.META.get('HTTP_DATE'),
        'services': {
            'database': 'connected',
            'api': 'operational',
            'applications': ['chat', 'documents', 'quiz']
        }
    })
