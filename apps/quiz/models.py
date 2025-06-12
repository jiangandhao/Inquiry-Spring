from django.db import models
from django.contrib.auth.models import User
from apps.documents.models import Document


class Quiz(models.Model):
    """测验集合模型"""
    
    DIFFICULTY_CHOICES = [
        (1, '简单'),
        (2, '中等'),
        (3, '困难'),
        (4, '大师'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name='创建用户',
        null=True,
        blank=True
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name='关联文档',
        null=True,
        blank=True
    )
    title = models.CharField('测验标题', max_length=200)
    description = models.TextField('测验描述', blank=True)
    difficulty_level = models.IntegerField('难度级别', choices=DIFFICULTY_CHOICES, default=2)
    time_limit = models.IntegerField('时间限制(秒)', default=1800)  # 30分钟
    passing_score = models.IntegerField('及格分数', default=60)

    # 配置信息
    metadata = models.JSONField('元数据', default=dict, blank=True)

    # 状态
    is_active = models.BooleanField('是否激活', default=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '测验'
        verbose_name_plural = '测验'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.document:
            return f"{self.title} ({self.document.title})"
        return f"{self.title} (无文档)"


class Question(models.Model):
    """题目模型"""
    
    QUESTION_TYPES = [
        ('MC', '单选题'),
        ('MCM', '多选题'),
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
    text = models.TextField('题目内容', default='默认题目内容')
    content = models.TextField('题目内容', default='默认题目内容')  # 保持兼容性
    question_type = models.CharField('题目类型', max_length=3, choices=QUESTION_TYPES)

    # 选项（JSON格式存储）
    options = models.JSONField('选项', null=True, blank=True)

    # 答案
    correct_answer = models.JSONField('正确答案')
    explanation = models.TextField('解释说明')

    # 来源信息
    source_passage = models.TextField('来源段落', blank=True)
    knowledge_points = models.JSONField('知识点', default=list, blank=True)

    # 难度和排序
    difficulty = models.IntegerField('难度', default=1)
    points = models.IntegerField('分值', default=10)
    order = models.PositiveIntegerField('排序', default=0)

    # 元数据
    metadata = models.JSONField('元数据', default=dict, blank=True)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
        ordering = ['quiz', 'order']
    
    def __str__(self):
        return f"{self.get_question_type_display()}: {self.content[:50]}..."


class QuizAttempt(models.Model):
    """测验答题记录"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name='用户',
        null=True,
        blank=True
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='测验'
    )

    # 答题信息
    answers_data = models.JSONField('答案记录', default=dict)
    score = models.FloatField('得分', default=0.0)
    total_questions = models.IntegerField('总题数', default=0)
    correct_answers = models.IntegerField('正确答案数', default=0)

    # 时间记录
    started_at = models.DateTimeField('开始时间', auto_now_add=True)
    completed_at = models.DateTimeField('完成时间', null=True, blank=True)
    time_taken = models.FloatField('用时(秒)', null=True, blank=True)

    # 状态
    is_completed = models.BooleanField('是否完成', default=False)
    
    class Meta:
        verbose_name = '答题记录'
        verbose_name_plural = '答题记录'
        ordering = ['-started_at']

    def __str__(self):
        return f"测验: {self.quiz.title} - 得分: {self.score}"

    @property
    def accuracy(self):
        """正确率"""
        if self.total_questions > 0:
            return round((self.correct_answers / self.total_questions) * 100, 2)
        return 0
