from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum, Count

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination

from .models import Document, DocumentChunk
from .serializers import (
    DocumentListSerializer, DocumentDetailSerializer,
    DocumentCreateSerializer, DocumentUpdateSerializer,
    DocumentChunkSerializer, DocumentChunkCreateSerializer,
    DocumentSearchSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """标准分页器"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ==================== 前端类视图已移除 ====================
# 前端开发由其他团队负责


# ==================== API 根视图 ====================

@api_view(['GET'])
@permission_classes([AllowAny])
def documents_api_root(request):
    """Documents应用API根视图"""
    return Response({
        'message': 'Documents API - 文档管理系统',
        'version': '1.0',
        'endpoints': {
            'documents': {
                'list': request.build_absolute_uri('/api/v1/documents/documents/'),
                'create': request.build_absolute_uri('/api/v1/documents/documents/'),
                'detail': request.build_absolute_uri('/api/v1/documents/documents/{id}/'),
                'search': request.build_absolute_uri('/api/v1/documents/documents/search/'),
                'statistics': request.build_absolute_uri('/api/v1/documents/documents/statistics/'),
                'process': request.build_absolute_uri('/api/v1/documents/documents/{id}/process/'),
            },
            'chunks': {
                'list': request.build_absolute_uri('/api/v1/documents/documents/{document_id}/chunks/'),
                'create': request.build_absolute_uri('/api/v1/documents/documents/{document_id}/chunks/'),
            }
        },
        'documentation': 'https://github.com/your-repo/wiki/documents-api'
    })


# ==================== REST API 视图 ====================

class DocumentListAPIView(generics.ListCreateAPIView):
    """文档列表API视图"""
    serializer_class = DocumentListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        queryset = Document.objects.prefetch_related('chunks', 'conversations')

        # 如果用户已认证，只返回该用户的文档
        # 注意：当前Document模型没有user字段，所以暂时返回所有文档
        # if self.request.user.is_authenticated:
        #     queryset = queryset.filter(user=self.request.user)

        # 过滤参数
        file_type = self.request.query_params.get('file_type')
        if file_type:
            queryset = queryset.filter(file_type=file_type)

        is_processed = self.request.query_params.get('is_processed')
        if is_processed is not None:
            queryset = queryset.filter(is_processed=is_processed.lower() == 'true')

        # 搜索
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search)
            ).distinct()

        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return DocumentCreateSerializer
        return DocumentListSerializer


class DocumentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """文档详情API视图"""
    serializer_class = DocumentDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        queryset = Document.objects.prefetch_related('chunks')

        # 如果用户已认证，只返回该用户的文档
        # 注意：当前Document模型没有user字段，所以暂时返回所有文档
        # if self.request.user.is_authenticated:
        #     queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method in ['PUT', 'PATCH']:
            return DocumentUpdateSerializer
        return DocumentDetailSerializer


class DocumentChunkListAPIView(generics.ListCreateAPIView):
    """文档片段列表API视图"""
    serializer_class = DocumentChunkSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        """获取查询集"""
        document_id = self.kwargs.get('document_id')
        if not document_id:
            return DocumentChunk.objects.none()

        queryset = DocumentChunk.objects.filter(document_id=document_id).select_related('document')

        # 如果用户已认证，只返回该用户的文档片段
        # 注意：当前Document模型没有user字段，所以暂时返回所有文档片段
        # if self.request.user.is_authenticated:
        #     queryset = queryset.filter(document__user=self.request.user)

        return queryset.order_by('chunk_index')

    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return DocumentChunkCreateSerializer
        return DocumentChunkSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def document_search_api_view(request):
    """文档搜索API视图"""
    try:
        serializer = DocumentSearchSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        queryset = Document.objects.all()

        # 如果用户已认证，只搜索该用户的文档
        # 注意：当前Document模型没有user字段，所以暂时搜索所有文档
        # if request.user.is_authenticated:
        #     queryset = queryset.filter(user=request.user)

        # 应用搜索条件
        if data.get('query'):
            queryset = queryset.filter(
                Q(title__icontains=data['query']) |
                Q(content__icontains=data['query'])
            ).distinct()

        if data.get('file_type'):
            queryset = queryset.filter(file_type=data['file_type'])

        if data.get('user_id'):
            queryset = queryset.filter(user_id=data['user_id'])

        if data.get('start_date'):
            queryset = queryset.filter(created_at__gte=data['start_date'])

        if data.get('end_date'):
            queryset = queryset.filter(created_at__lte=data['end_date'])

        if data.get('is_processed') is not None:
            queryset = queryset.filter(is_processed=data['is_processed'])

        if data.get('min_size'):
            queryset = queryset.filter(file_size__gte=data['min_size'])

        if data.get('max_size'):
            queryset = queryset.filter(file_size__lte=data['max_size'])

        # 分页
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset.order_by('-created_at'), request)

        if page is not None:
            serializer = DocumentListSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = DocumentListSerializer(queryset.order_by('-created_at'), many=True)
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
def document_statistics_api_view(request):
    """文档统计API视图"""
    try:
        queryset = Document.objects.all()

        # 如果用户已认证，只统计该用户的文档
        if request.user.is_authenticated:
            queryset = queryset.filter(user=request.user)

        # 基本统计
        total_documents = queryset.count()
        processed_documents = queryset.filter(is_processed=True).count()
        total_chunks = DocumentChunk.objects.filter(document__in=queryset).count()
        total_size = queryset.aggregate(total=Sum('file_size'))['total'] or 0

        # 按文件类型统计
        file_type_stats = {}
        file_types = queryset.values('file_type').annotate(count=Count('id'))
        for item in file_types:
            file_type_stats[item['file_type']] = item['count']

        # 最近文档
        recent_documents = queryset.order_by('-created_at')[:5]
        recent_data = DocumentListSerializer(recent_documents, many=True).data

        return Response({
            'success': True,
            'data': {
                'total_documents': total_documents,
                'processed_documents': processed_documents,
                'total_chunks': total_chunks,
                'total_size': total_size,
                'file_type_stats': file_type_stats,
                'recent_documents': recent_data
            }
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def document_process_api_view(request, document_id):
    """文档处理API视图"""
    try:
        document = get_object_or_404(Document, id=document_id)

        # 如果用户已认证，检查权限
        if request.user.is_authenticated and document.user != request.user:
            return Response({'error': '无权限操作此文档'}, status=status.HTTP_403_FORBIDDEN)

        if document.is_processed:
            return Response({
                'success': False,
                'message': '文档已经处理过了'
            }, status=status.HTTP_400_BAD_REQUEST)

        # TODO: 实现文档处理逻辑
        # 这里可以集成AI服务进行文档分析和分块

        # 模拟处理过程
        document.is_processed = True
        document.save()

        return Response({
            'success': True,
            'message': '文档处理完成',
            'document_id': document.id
        })

    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
