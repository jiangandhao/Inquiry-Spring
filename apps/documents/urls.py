from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # ==================== Documents API 端点 ====================
    # 按照Django最佳实践组织API结构

    # API根视图
    path('', views.documents_api_root, name='api_root'),

    # 文档管理API
    path('documents/', views.DocumentListAPIView.as_view(), name='document_list'),
    path('documents/<int:pk>/', views.DocumentDetailAPIView.as_view(), name='document_detail'),
    path('documents/search/', views.document_search_api_view, name='document_search'),
    path('documents/statistics/', views.document_statistics_api_view, name='document_statistics'),
    path('documents/<int:document_id>/process/', views.document_process_api_view, name='document_process'),

    # 文档分块API
    path('documents/<int:document_id>/chunks/', views.DocumentChunkListAPIView.as_view(), name='document_chunk_list'),

    # 兼容性路由（保持向后兼容）
    path('api/documents/', views.DocumentListAPIView.as_view(), name='api_document_list'),
    path('api/documents/<int:pk>/', views.DocumentDetailAPIView.as_view(), name='api_document_detail'),
    path('api/documents/search/', views.document_search_api_view, name='api_document_search'),
    path('api/documents/statistics/', views.document_statistics_api_view, name='api_document_statistics'),
    path('api/documents/<int:document_id>/process/', views.document_process_api_view, name='api_document_process'),
    path('api/documents/<int:document_id>/chunks/', views.DocumentChunkListAPIView.as_view(), name='api_document_chunk_list'),
]
