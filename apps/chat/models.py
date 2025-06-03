from django.db import models
from django.contrib.auth.models import User
from apps.documents.models import Document


class Conversation(models.Model):
    """对话会话模型"""
    
    MODE_CHOICES = [
        ('chat', '聊天模式'),
        ('summary', '总结模式'),
        ('quiz', '测验模式'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations',
        verbose_name='用户',
        null=True,
        blank=True
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='conversations',
        verbose_name='关联文档',
        null=True,
        blank=True
    )

    title = models.CharField('对话标题', max_length=200, blank=True)
    mode = models.CharField('交互模式', max_length=20, choices=MODE_CHOICES, default='chat')
    
    # 上下文信息
    context = models.JSONField('对话上下文', default=dict, blank=True)
    
    # 状态
    is_active = models.BooleanField('是否激活', default=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '对话会话'
        verbose_name_plural = '对话会话'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['user', '-updated_at']),
            models.Index(fields=['document', '-updated_at']),
            models.Index(fields=['mode', '-updated_at']),
        ]
    
    def __str__(self):
        title = self.title or f"对话-{self.id}"
        return f"{title} ({self.get_mode_display()})"
    
    def save(self, *args, **kwargs):
        # 自动生成标题
        if not self.title:
            if self.document:
                self.title = f"{self.document.title} - {self.get_mode_display()}"
            else:
                self.title = f"通用{self.get_mode_display()}"
        super().save(*args, **kwargs)


class Message(models.Model):
    """消息模型"""
    
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages',
        verbose_name='所属对话'
    )
    
    content = models.TextField('消息内容')
    is_user = models.BooleanField('是否为用户消息', default=True)
    
    # 元数据信息
    metadata = models.JSONField('元数据', default=dict, blank=True)
    
    # 反馈信息
    feedback_score = models.IntegerField(
        '反馈评分', 
        null=True, 
        blank=True,
        choices=[(1, '差'), (2, '一般'), (3, '好'), (4, '很好'), (5, '优秀')]
    )
    feedback_comment = models.TextField('反馈评论', blank=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['conversation', 'created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['is_user', 'created_at']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        sender = "用户" if self.is_user else "AI"
        return f"{sender}: {self.content[:50]}..."


class MessageSource(models.Model):
    """消息来源引用模型"""
    
    message = models.ForeignKey(
        Message, 
        on_delete=models.CASCADE, 
        related_name='sources',
        verbose_name='关联消息'
    )
    
    # 来源信息
    source_type = models.CharField(
        '来源类型', 
        max_length=20, 
        choices=[('document', '文档'), ('chunk', '文档片段')],
        default='document'
    )
    source_id = models.PositiveIntegerField('来源ID')
    source_content = models.TextField('来源内容')
    
    # 相关性评分
    relevance_score = models.FloatField('相关性评分', default=0.0)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '消息来源'
        verbose_name_plural = '消息来源'
        ordering = ['-relevance_score']
    
    def __str__(self):
        return f"{self.get_source_type_display()}-{self.source_id} (相关性: {self.relevance_score})"
