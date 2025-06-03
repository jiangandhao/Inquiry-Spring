from django.db import models
from apps.documents.models import Document


class Quiz(models.Model):
    """测验集合模型"""
    
    DIFFICULTY_CHOICES = [
        (1, '简单'),
        (2, '中等'),
        (3, '困难'),
    ]
    
    document = models.ForeignKey(
        Document, 
        on_delete=models.CASCADE, 
        related_name='quizzes',
        verbose_name='关联文档'
    )
    title = models.CharField('测验标题', max_length=200)
    description = models.TextField('测验描述', blank=True)
    difficulty_level = models.IntegerField('难度级别', choices=DIFFICULTY_CHOICES, default=2)
    total_questions = models.PositiveIntegerField('题目总数', default=0)
    
    # 配置信息
    config = models.JSONField('生成配置', default=dict, blank=True)
    
    # 状态
    is_active = models.BooleanField('是否激活', default=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '测验'
        verbose_name_plural = '测验'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.document.title})"


class Question(models.Model):
    """题目模型"""
    
    QUESTION_TYPES = [
        ('MC', '选择题'),
        ('TF', '判断题'),
        ('FB', '填空题'),
        ('SA', '简答题'),
    ]
    
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='questions',
        verbose_name='所属测验'
    )
    content = models.TextField('题目内容')
    question_type = models.CharField('题目类型', max_length=2, choices=QUESTION_TYPES)
    
    # 选项（JSON格式存储）
    options = models.JSONField('选项', null=True, blank=True)
    
    # 答案
    correct_answer = models.TextField('正确答案')
    explanation = models.TextField('解释说明')
    
    # 来源信息
    source_passage = models.TextField('来源段落', blank=True)
    knowledge_points = models.JSONField('知识点', default=list, blank=True)
    
    # 难度和排序
    difficulty = models.IntegerField('难度', default=1)
    order = models.PositiveIntegerField('排序', default=0)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['quiz', 'order']
    
    def __str__(self):
        return f"{self.get_question_type_display()}: {self.content[:50]}..."


class QuizAttempt(models.Model):
    """测验答题记录"""
    
    quiz = models.ForeignKey(
        Quiz, 
        on_delete=models.CASCADE, 
        related_name='attempts',
        verbose_name='测验'
    )
    
    # 答题信息
    answers = models.JSONField('答案记录', default=dict)
    score = models.FloatField('得分', default=0.0)
    total_score = models.FloatField('总分', default=0.0)
    
    # 时间记录
    start_time = models.DateTimeField('开始时间', auto_now_add=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    duration = models.DurationField('答题时长', null=True, blank=True)
    
    # 状态
    is_completed = models.BooleanField('是否完成', default=False)
    
    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"测验: {self.quiz.title} - 得分: {self.score}/{self.total_score}"
    
    @property
    def accuracy(self):
        """正确率"""
        if self.total_score > 0:
            return round((self.score / self.total_score) * 100, 2)
        return 0
