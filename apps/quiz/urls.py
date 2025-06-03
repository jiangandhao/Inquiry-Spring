from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    # ==================== Quiz API 端点 ====================
    # 按照Django最佳实践组织API结构

    # API根视图
    path('', views.quiz_api_root, name='api_root'),

    # 测验管理API
    path('quizzes/', views.QuizListAPIView.as_view(), name='quiz_list'),
    path('quizzes/<int:pk>/', views.QuizDetailAPIView.as_view(), name='quiz_detail'),
    path('quizzes/search/', views.quiz_search_api_view, name='quiz_search'),
    path('quizzes/statistics/', views.quiz_statistics_api_view, name='quiz_statistics'),

    # 问题管理API
    path('quizzes/<int:quiz_id>/questions/', views.QuestionListAPIView.as_view(), name='question_list'),

    # 测验尝试API
    path('quizzes/<int:quiz_id>/attempts/', views.QuizAttemptListAPIView.as_view(), name='quiz_attempt_list'),
    path('attempts/', views.QuizAttemptListAPIView.as_view(), name='attempt_list'),
    path('attempts/<int:attempt_id>/submit/', views.quiz_attempt_submit_api_view, name='attempt_submit'),

    # 兼容性路由（保持向后兼容）
    path('api/quizzes/', views.QuizListAPIView.as_view(), name='api_quiz_list'),
    path('api/quizzes/<int:pk>/', views.QuizDetailAPIView.as_view(), name='api_quiz_detail'),
    path('api/quizzes/search/', views.quiz_search_api_view, name='api_quiz_search'),
    path('api/quizzes/statistics/', views.quiz_statistics_api_view, name='api_quiz_statistics'),
    path('api/quizzes/<int:quiz_id>/questions/', views.QuestionListAPIView.as_view(), name='api_question_list'),
    path('api/quizzes/<int:quiz_id>/attempts/', views.QuizAttemptListAPIView.as_view(), name='api_quiz_attempt_list'),
    path('api/attempts/', views.QuizAttemptListAPIView.as_view(), name='api_attempt_list'),
    path('api/attempts/<int:attempt_id>/submit/', views.quiz_attempt_submit_api_view, name='api_attempt_submit'),
]
