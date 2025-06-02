from django.shortcuts import get_object_or_404
from django.db.models import Q, Avg, Count
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .models import Quiz, Question, QuizAttempt
from .serializers import (
    QuizListSerializer, QuizDetailSerializer, QuizCreateSerializer,
    QuestionSerializer, QuestionCreateSerializer,
    QuizAttemptSerializer, QuizAttemptCreateSerializer, QuizAttemptSubmitSerializer,
    QuizSearchSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """标准分页器"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ==================== API 根视图 ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_api_root(request):
    """Quiz应用API根视图"""
    return Response({
        'message': 'Quiz API - 测验管理系统',
        'version': '1.0',
        'endpoints': {
            'quizzes': {
                'list': request.build_absolute_uri('/api/v1/quiz/quizzes/'),
                'create': request.build_absolute_uri('/api/v1/quiz/quizzes/'),
                'detail': request.build_absolute_uri('/api/v1/quiz/quizzes/{id}/'),
                'search': request.build_absolute_uri('/api/v1/quiz/quizzes/search/'),
                'statistics': request.build_absolute_uri('/api/v1/quiz/quizzes/statistics/'),
            },
            'questions': {
                'list': request.build_absolute_uri('/api/v1/quiz/quizzes/{quiz_id}/questions/'),
                'create': request.build_absolute_uri('/api/v1/quiz/quizzes/{quiz_id}/questions/'),
            },
            'attempts': {
                'list': request.build_absolute_uri('/api/v1/quiz/attempts/'),
                'create': request.build_absolute_uri('/api/v1/quiz/quizzes/{quiz_id}/attempts/'),
                'submit': request.build_absolute_uri('/api/v1/quiz/attempts/{attempt_id}/submit/'),
            }
        },
        'documentation': 'https://github.com/your-repo/wiki/quiz-api'
    })


# ==================== REST API 视图 ====================

class QuizListAPIView(generics.ListCreateAPIView):
    """测验列表API视图"""
    serializer_class = QuizListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        queryset = Quiz.objects.select_related('user', 'document').prefetch_related('questions', 'attempts')

        # 如果用户已认证，只返回该用户的测验
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        # 过滤参数
        difficulty_level = self.request.query_params.get('difficulty_level')
        if difficulty_level:
            queryset = queryset.filter(difficulty_level=difficulty_level)

        document_id = self.request.query_params.get('document_id')
        if document_id:
            queryset = queryset.filter(document_id=document_id)

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            ).distinct()

        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return QuizCreateSerializer
        return QuizListSerializer


class QuizDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """测验详情API视图"""
    serializer_class = QuizDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        queryset = Quiz.objects.select_related('user', 'document').prefetch_related('questions__answers')

        # 如果用户已认证，只返回该用户的测验
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class QuestionListAPIView(generics.ListCreateAPIView):
    """问题列表API视图"""
    serializer_class = QuestionSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        quiz_id = self.kwargs.get('quiz_id')
        if not quiz_id:
            return Question.objects.none()

        queryset = Question.objects.filter(quiz_id=quiz_id).select_related('quiz').prefetch_related('answers')

        # 如果用户已认证，只返回该用户的测验问题
        if self.request.user.is_authenticated:
            queryset = queryset.filter(quiz__user=self.request.user)

        return queryset.order_by('id')

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionSerializer


class QuizAttemptListAPIView(generics.ListCreateAPIView):
    """测验尝试列表API视图"""
    serializer_class = QuizAttemptSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        quiz_id = self.kwargs.get('quiz_id')
        if quiz_id:
            queryset = QuizAttempt.objects.filter(quiz_id=quiz_id)
        else:
            queryset = QuizAttempt.objects.all()

        queryset = queryset.select_related('user', 'quiz')

        # 如果用户已认证，只返回该用户的尝试记录
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset.order_by('-started_at')

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return QuizAttemptCreateSerializer
        return QuizAttemptSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def quiz_attempt_submit_api_view(request, attempt_id):
    """提交测验答案API视图"""
    try:
        attempt = get_object_or_404(QuizAttempt, id=attempt_id)

        # 如果用户已认证，检查权限
        if request.user.is_authenticated and attempt.user != request.user:
            return Response({'error': '无权限操作此测验尝试'}, status=status.HTTP_403_FORBIDDEN)

        if attempt.is_completed:
            return Response({
                'success': False,
                'message': '测验已经完成，不能重复提交'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = QuizAttemptSubmitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        answers_data = serializer.validated_data['answers']

        # 计算得分
        quiz = attempt.quiz
        questions = quiz.questions.all()

        correct_count = 0
        total_score = 0
        results = []

        for question in questions:
            user_answers = answers_data.get(str(question.id), [])
            correct_answers = question.correct_answer

            # 简单的答案比较（根据实际需求可以更复杂）
            is_correct = user_answers == correct_answers
            points = 10  # 默认每题10分，可以根据question.difficulty调整

            if is_correct:
                correct_count += 1
                total_score += points

            results.append({
                'question_id': question.id,
                'question_text': question.content,
                'user_answers': user_answers,
                'correct_answers': correct_answers,
                'is_correct': is_correct,
                'points': points if is_correct else 0,
                'explanation': question.explanation
            })

        # 更新尝试记录
        attempt.answers_data = answers_data
        attempt.correct_answers = correct_count
        attempt.score = total_score
        attempt.is_completed = True
        attempt.completed_at = timezone.now()

        if attempt.started_at:
            attempt.time_taken = (attempt.completed_at - attempt.started_at).total_seconds()

        attempt.save()

        return Response({
            'success': True,
            'attempt_id': attempt.id,
            'score': total_score,
            'correct_answers': correct_count,
            'total_questions': attempt.total_questions,
            'accuracy': (correct_count / attempt.total_questions * 100) if attempt.total_questions > 0 else 0,
            'time_taken': attempt.time_taken,
            'results': results
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_search_api_view(request):
    """测验搜索API视图"""
    try:
        serializer = QuizSearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        queryset = Quiz.objects.select_related('user', 'document')

        # 如果用户已认证，只搜索该用户的测验
        if request.user.is_authenticated:
            queryset = queryset.filter(user=request.user)

        # 应用搜索条件
        if data.get('query'):
            queryset = queryset.filter(
                Q(title__icontains=data['query']) |
                Q(description__icontains=data['query'])
            ).distinct()

        if data.get('difficulty_level'):
            queryset = queryset.filter(difficulty_level=data['difficulty_level'])

        if data.get('document_id'):
            queryset = queryset.filter(document_id=data['document_id'])

        if data.get('user_id'):
            queryset = queryset.filter(user_id=data['user_id'])

        if data.get('start_date'):
            queryset = queryset.filter(created_at__gte=data['start_date'])

        if data.get('end_date'):
            queryset = queryset.filter(created_at__lte=data['end_date'])

        if data.get('is_active') is not None:
            queryset = queryset.filter(is_active=data['is_active'])

        # 按问题数量过滤
        if data.get('min_questions') or data.get('max_questions'):
            queryset = queryset.annotate(question_count=Count('questions'))

            if data.get('min_questions'):
                queryset = queryset.filter(question_count__gte=data['min_questions'])

            if data.get('max_questions'):
                queryset = queryset.filter(question_count__lte=data['max_questions'])

        # 分页
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset.order_by('-created_at'), request)

        if page is not None:
            serializer = QuizListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = QuizListSerializer(queryset.order_by('-created_at'), many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_statistics_api_view(request):
    """测验统计API视图"""
    try:
        queryset = Quiz.objects.all()

        # 如果用户已认证，只统计该用户的测验
        if request.user.is_authenticated:
            queryset = queryset.filter(user=request.user)

        # 基本统计
        total_quizzes = queryset.count()
        active_quizzes = queryset.filter(is_active=True).count()
        total_questions = Question.objects.filter(quiz__in=queryset).count()

        # 尝试统计
        attempts_queryset = QuizAttempt.objects.filter(quiz__in=queryset)
        total_attempts = attempts_queryset.count()
        completed_attempts = attempts_queryset.filter(is_completed=True).count()

        # 平均分数
        avg_score = attempts_queryset.filter(is_completed=True).aggregate(avg=Avg('score'))['avg'] or 0

        # 按难度统计
        difficulty_stats = {}
        for choice in Quiz.DIFFICULTY_CHOICES:
            difficulty = choice[0]
            count = queryset.filter(difficulty_level=difficulty).count()
            difficulty_stats[choice[1]] = count

        # 最近测验
        recent_quizzes = queryset.order_by('-created_at')[:5]
        recent_data = QuizListSerializer(recent_quizzes, many=True).data

        return Response({
            'success': True,
            'data': {
                'total_quizzes': total_quizzes,
                'active_quizzes': active_quizzes,
                'total_questions': total_questions,
                'total_attempts': total_attempts,
                'completed_attempts': completed_attempts,
                'average_score': round(avg_score, 2),
                'difficulty_stats': difficulty_stats,
                'recent_quizzes': recent_data
            }
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
