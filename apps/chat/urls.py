from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # 对话列表和详情
    path('conversations/', views.ConversationListView.as_view(), name='conversation_list'),
    path('conversations/<int:pk>/', views.ConversationDetailView.as_view(), name='conversation_detail'),
    
    # 聊天接口
    path('', views.chat_interface_view, name='chat_interface'),
    path('api/', views.chat_view, name='chat_api'),
    
    # 反馈接口
    path('feedback/', views.conversation_feedback_view, name='conversation_feedback'),
]
