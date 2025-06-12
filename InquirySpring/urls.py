"""
URL configuration for InquirySpring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
import api_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # ==================== API 路由 ====================
    # 按照Django最佳实践，将API划分到各自的应用中

    # 主API根视图
    path('api/', api_views.api_root, name='api_root'),
    path('api/health/', api_views.api_health, name='api_health'),

    # API v1 路由
    path('api/v1/chat/', include('apps.chat.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),
    path('api/v1/quiz/', include('apps.quiz.urls')),

    # 兼容性路由（保持向后兼容）
    path('chat/', include('apps.chat.urls')),
    path('documents/', include('apps.documents.urls')),
    path('quiz/', include('apps.quiz.urls')),
]

# ==================== 静态文件服务已移除 ====================
# 前端开发由其他团队负责，本项目专注于API设计
# 如需要媒体文件服务，可以取消注释以下代码：
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
