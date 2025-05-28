from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
import json

from .models import Conversation, Message, MessageSource
from apps.documents.models import Document


class ConversationListView(ListView):
    """对话列表视图"""
    model = Conversation
    template_name = 'chat/conversation_list.html'
    context_object_name = 'conversations'
    paginate_by = 10


class ConversationDetailView(DetailView):
    """对话详情视图"""
    model = Conversation
    template_name = 'chat/conversation_detail.html'
    context_object_name = 'conversation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all()
        return context


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


def chat_interface_view(request):
    """聊天界面视图"""
    documents = Document.objects.all()
    recent_conversations = Conversation.objects.all()[:10]
    
    context = {
        'documents': documents,
        'recent_conversations': recent_conversations,
        'mode_choices': Conversation.MODE_CHOICES,
    }
    
    return render(request, 'chat/chat_interface.html', context)


@csrf_exempt
def conversation_feedback_view(request):
    """对话反馈视图"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_id = data.get('message_id')
            feedback_score = data.get('feedback_score')
            feedback_comment = data.get('feedback_comment', '')
            
            message = get_object_or_404(Message, id=message_id)
            
            # 更新反馈信息
            message.feedback_score = feedback_score
            message.feedback_comment = feedback_comment
            message.save()
            
            return JsonResponse({
                'success': True,
                'message': '反馈提交成功'
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': '仅支持POST请求'}, status=405)
