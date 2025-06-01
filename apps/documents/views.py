from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import Document, DocumentChunk


class DocumentListView(ListView):
    """文档列表视图"""
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        return Document.objects.all().order_by('-created_at')


class DocumentDetailView(DetailView):
    """文档详情视图"""
    model = Document
    template_name = 'documents/document_detail.html'
    context_object_name = 'document'


@method_decorator(csrf_exempt, name='dispatch')
class DocumentUploadView(View):
    """文档上传视图"""
    
    def post(self, request):
        try:
            # 获取上传的文件
            uploaded_file = request.FILES.get('file')
            title = request.POST.get('title', '')
            
            if not uploaded_file:
                return JsonResponse({'error': '请选择文件'}, status=400)
            
            if not title:
                title = uploaded_file.name
            
            # 创建文档记录
            document = Document.objects.create(
                title=title,
                file=uploaded_file
            )
            
            return JsonResponse({
                'success': True,
                'document_id': document.id,
                'message': '文件上传成功'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def document_summary_view(request, document_id):
    """文档总结视图"""
    document = get_object_or_404(Document, id=document_id)
    
    # TODO: 集成AI服务生成总结
    summary = "这里将显示AI生成的文档总结..."
    
    return JsonResponse({
        'document_id': document.id,
        'title': document.title,
        'summary': summary
    })


def home_view(request):
    """首页视图"""
    recent_documents = Document.objects.all()[:5]
    
    context = {
        'recent_documents': recent_documents,
        'total_documents': Document.objects.count(),
    }
    
    return render(request, 'home.html', context)
