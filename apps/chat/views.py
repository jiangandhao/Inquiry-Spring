from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Prefetch
from datetime import datetime
import json

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .models import Conversation, Message
from .serializers import (
    ConversationListSerializer, ConversationDetailSerializer,
    ConversationCreateSerializer, MessageSerializer,
    MessageCreateSerializer, MessageFeedbackSerializer
)
from apps.documents.models import Document


class StandardResultsSetPagination(PageNumberPagination):
    """标准分页器"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ==================== 前端类视图已移除 ====================
# 前端开发由其他团队负责


@csrf_exempt
def chat_view(request):
    """聊天接口视图"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_content = data.get('message', '')
            document_id = data.get('document_id')
            conversation_id = data.get('conversation_id')
            mode = data.get('mode', 'chat')
            
            if not message_content:
                return JsonResponse({'error': '消息内容不能为空'}, status=400)
            
            # 获取或创建对话
            if conversation_id:
                conversation = get_object_or_404(Conversation, id=conversation_id)
            else:
                document = None
                if document_id:
                    document = get_object_or_404(Document, id=document_id)
                
                conversation = Conversation.objects.create(
                    document=document,
                    mode=mode
                )
            
            # 保存用户消息
            user_message = Message.objects.create(
                conversation=conversation,
                content=message_content,
                is_user=True
            )
            
            # TODO: 集成AI服务生成回复
            # 这里先返回示例回复
            ai_response = f"这是对您问题「{message_content}」的AI回复。"
            
            if conversation.document:
                ai_response += f"\n\n基于文档「{conversation.document.title}」的内容..."
            
            # 保存AI回复
            ai_message = Message.objects.create(
                conversation=conversation,
                content=ai_response,
                is_user=False
            )
            
            return JsonResponse({
                'success': True,
                'conversation_id': conversation.id,
                'user_message_id': user_message.id,
                'ai_message_id': ai_message.id,
                'ai_response': ai_response
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '仅支持POST请求'}, status=405)


# ==================== API 根视图 ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def chat_api_root(request):
    """Chat应用API根视图"""
    return Response({
        'message': 'Chat API - 对话管理系统',
        'version': '1.0',
        'endpoints': {
            'conversations': {
                'list': request.build_absolute_uri('/api/v1/chat/conversations/'),
                'create': request.build_absolute_uri('/api/v1/chat/conversations/'),
                'detail': request.build_absolute_uri('/api/v1/chat/conversations/{id}/'),
                'history': request.build_absolute_uri('/api/v1/chat/conversations/history/'),
                'statistics': request.build_absolute_uri('/api/v1/chat/conversations/statistics/'),
            },
            'messages': {
                'list': request.build_absolute_uri('/api/v1/chat/conversations/{conversation_id}/messages/'),
                'create': request.build_absolute_uri('/api/v1/chat/conversations/{conversation_id}/messages/'),
                'detail': request.build_absolute_uri('/api/v1/chat/messages/{id}/'),
                'feedback': request.build_absolute_uri('/api/v1/chat/messages/{message_id}/feedback/'),
            }
        },
        'documentation': 'https://github.com/your-repo/wiki/chat-api'
    })


# ==================== REST API 视图 ====================

class ConversationListAPIView(generics.ListCreateAPIView):
    """对话列表API视图"""
    serializer_class = ConversationListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]  # 暂时允许所有用户访问

    def get_queryset(self):
        """获取查询集"""
        queryset = Conversation.objects.select_related('user', 'document').prefetch_related(
            Prefetch('messages', queryset=Message.objects.order_by('created_at'))
        )

        # 如果用户已认证，只返回该用户的对话
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        # 过滤参数
        mode = self.request.query_params.get('mode')
        if mode:
            queryset = queryset.filter(mode=mode)

        document_id = self.request.query_params.get('document_id')
        if document_id:
            queryset = queryset.filter(document_id=document_id)

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # 时间范围过滤
        start_date = self.request.query_params.get('start_date')
        if start_date:
            try:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__gte=start_date)
            except ValueError:
                pass

        end_date = self.request.query_params.get('end_date')
        if end_date:
            try:
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                queryset = queryset.filter(created_at__lte=end_date)
            except ValueError:
                pass

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(messages__content__icontains=search)
            ).distinct()

        return queryset.order_by('-updated_at')

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return ConversationCreateSerializer
        return ConversationListSerializer


class ConversationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """对话详情API视图"""
    serializer_class = ConversationDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        queryset = Conversation.objects.select_related('user', 'document').prefetch_related(
            'messages__conversation'
        )

        # 如果用户已认证，只返回该用户的对话
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MessageListAPIView(generics.ListCreateAPIView):
    """消息列表API视图"""
    serializer_class = MessageSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        conversation_id = self.kwargs.get('conversation_id')
        if not conversation_id:
            return Message.objects.none()

        queryset = Message.objects.filter(conversation_id=conversation_id).select_related('conversation')

        # 如果用户已认证，只返回该用户的对话消息
        if self.request.user.is_authenticated:
            queryset = queryset.filter(conversation__user=self.request.user)

        # 过滤参数
        is_user = self.request.query_params.get('is_user')
        if is_user is not None:
            queryset = queryset.filter(is_user=is_user.lower() == 'true')

        return queryset.order_by('created_at')

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer


class MessageDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """消息详情API视图"""
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        queryset = Message.objects.select_related('conversation')

        # 如果用户已认证，只返回该用户的消息
        if self.request.user.is_authenticated:
            queryset = queryset.filter(conversation__user=self.request.user)

        return queryset


@api_view(['GET'])
@permission_classes([AllowAny])
def conversation_history_api_view(request):
    """获取对话历史API视图"""
    try:
        # 获取查询参数
        page_size = int(request.query_params.get('page_size', 20))
        mode = request.query_params.get('mode')
        search = request.query_params.get('search')

        # 构建查询集
        queryset = Conversation.objects.select_related('user', 'document').prefetch_related('messages')

        # 如果用户已认证，只返回该用户的对话
        if request.user.is_authenticated:
            queryset = queryset.filter(user=request.user)

        # 应用过滤条件
        if mode:
            queryset = queryset.filter(mode=mode)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(messages__content__icontains=search)
            ).distinct()

        # 排序
        queryset = queryset.order_by('-updated_at')

        # 分页
        paginator = StandardResultsSetPagination()
        paginator.page_size = page_size
        page_obj = paginator.paginate_queryset(queryset, request)

        if page_obj is not None:
            serializer = ConversationListSerializer(page_obj, many=True)
            return paginator.get_paginated_response(serializer.data)

        # 如果没有分页，返回所有数据
        serializer = ConversationListSerializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': queryset.count()
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def message_feedback_api_view(request, message_id):
    """消息反馈API视图"""
    try:
        message = get_object_or_404(Message, id=message_id)

        # 如果用户已认证，检查权限
        if request.user.is_authenticated and message.conversation.user != request.user:
            return Response({'error': '无权限操作此消息'}, status=status.HTTP_403_FORBIDDEN)

        serializer = MessageFeedbackSerializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': '反馈提交成功',
                'data': serializer.data
            })

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def conversation_statistics_api_view(request):
    """对话统计API视图"""
    try:
        queryset = Conversation.objects.all()

        # 如果用户已认证，只统计该用户的对话
        if request.user.is_authenticated:
            queryset = queryset.filter(user=request.user)

        # 基本统计
        total_conversations = queryset.count()
        active_conversations = queryset.filter(is_active=True).count()

        # 按模式统计
        mode_stats = {}
        for mode_choice in Conversation.MODE_CHOICES:
            mode = mode_choice[0]
            count = queryset.filter(mode=mode).count()
            mode_stats[mode] = count

        # 消息统计
        total_messages = Message.objects.filter(conversation__in=queryset).count()
        user_messages = Message.objects.filter(conversation__in=queryset, is_user=True).count()
        ai_messages = total_messages - user_messages

        # 最近活动
        recent_conversations = queryset.order_by('-updated_at')[:5]
        recent_data = ConversationListSerializer(recent_conversations, many=True).data

        return Response({
            'success': True,
            'data': {
                'total_conversations': total_conversations,
                'active_conversations': active_conversations,
                'mode_statistics': mode_stats,
                'message_statistics': {
                    'total_messages': total_messages,
                    'user_messages': user_messages,
                    'ai_messages': ai_messages
                },
                'recent_conversations': recent_data
            }
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
