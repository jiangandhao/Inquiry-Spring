from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # ==================== Chat API 端点 ====================
    # 按照Django最佳实践组织API结构

    # API根视图
    path('', views.chat_api_root, name='api_root'),

    # 对话管理API
    path('conversations/', views.ConversationListAPIView.as_view(), name='conversation_list'),
    path('conversations/<int:pk>/', views.ConversationDetailAPIView.as_view(), name='conversation_detail'),
    path('conversations/history/', views.conversation_history_api_view, name='conversation_history'),
    path('conversations/statistics/', views.conversation_statistics_api_view, name='conversation_statistics'),

    # 消息管理API
    path('conversations/<int:conversation_id>/messages/', views.MessageListAPIView.as_view(), name='message_list'),
    path('messages/<int:pk>/', views.MessageDetailAPIView.as_view(), name='message_detail'),
    path('messages/<int:message_id>/feedback/', views.message_feedback_api_view, name='message_feedback'),

    # 兼容性路由（保持向后兼容）
    path('api/conversations/', views.ConversationListAPIView.as_view(), name='api_conversation_list'),
    path('api/conversations/<int:pk>/', views.ConversationDetailAPIView.as_view(), name='api_conversation_detail'),
    path('api/conversations/history/', views.conversation_history_api_view, name='api_conversation_history'),
    path('api/conversations/statistics/', views.conversation_statistics_api_view, name='api_conversation_statistics'),
    path('api/conversations/<int:conversation_id>/messages/', views.MessageListAPIView.as_view(), name='api_message_list'),
    path('api/messages/<int:pk>/', views.MessageDetailAPIView.as_view(), name='api_message_detail'),
    path('api/messages/<int:message_id>/feedback/', views.message_feedback_api_view, name='api_message_feedback'),
]
