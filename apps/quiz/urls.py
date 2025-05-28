from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # 测验列表和详情
    path('', views.QuizListView.as_view(), name='quiz_list'),
    path('<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    
    # 测验生成和配置
    path('form/', views.quiz_form_view, name='quiz_form'),
    path('generate/', views.quiz_generation_view, name='quiz_generate'),
    
    # 测验提交
    path('submit/', views.quiz_submission_view, name='quiz_submit'),
]
