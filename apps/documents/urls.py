from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # 文档列表和详情
    path('', views.DocumentListView.as_view(), name='document_list'),
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document_detail'),
    
    # 文档上传
    path('upload/', views.DocumentUploadView.as_view(), name='document_upload'),
    
    # 文档总结
    path('<int:document_id>/summary/', views.document_summary_view, name='document_summary'),
]
