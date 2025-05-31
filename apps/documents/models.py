from django.db import models
from django.core.validators import FileExtensionValidator
import os


class Document(models.Model):
    """文档模型"""
    
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'Word文档'),
        ('txt', '文本文件'),
        ('md', 'Markdown'),
    ]
    
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容', blank=True)
    file = models.FileField(
        '文件',
        upload_to='documents/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt', 'md'])],
        null=True,
        blank=True
    )
    file_type = models.CharField('文件类型', max_length=10, choices=FILE_TYPE_CHOICES)
    file_size = models.PositiveIntegerField('文件大小(字节)', default=0)
    metadata = models.JSONField('元数据', default=dict, blank=True)
    
    # 向量化相关字段
    vector_id = models.CharField('向量ID', max_length=100, null=True, blank=True)
    is_processed = models.BooleanField('是否已处理', default=False)
    
    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def file_size_mb(self):
        """返回文件大小(MB)"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    def save(self, *args, **kwargs):
        # 自动设置文件类型和大小
        if self.file:
            self.file_type = os.path.splitext(self.file.name)[1][1:].lower()
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class DocumentChunk(models.Model):
    """文档分块模型 - 用于向量存储"""
    
    document = models.ForeignKey(
        Document, 
        on_delete=models.CASCADE, 
        related_name='chunks',
        verbose_name='文档'
    )
    content = models.TextField('分块内容')
    chunk_index = models.PositiveIntegerField('分块索引')
    start_char = models.PositiveIntegerField('起始字符位置', default=0)
    end_char = models.PositiveIntegerField('结束字符位置', default=0)
    
    # 向量相关
    vector_id = models.CharField('向量ID', max_length=100, null=True, blank=True)
    embedding_model = models.CharField('嵌入模型', max_length=100, default='sentence-transformers')
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '文档分块'
        verbose_name_plural = '文档分块'
        ordering = ['document', 'chunk_index']
        unique_together = ['document', 'chunk_index']
    
    def __str__(self):
        return f"{self.document.title} - 分块{self.chunk_index}"
