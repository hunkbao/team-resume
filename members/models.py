from django.db import models


class Profile(models.Model):
    """个人简历信息模型"""

    POLITICAL_CHOICES = [
        ('群众', '群众'),
        ('共青团员', '共青团员'),
        ('中共党员', '中共党员'),
        ('中共预备党员', '中共预备党员'),
        ('民主党派', '民主党派'),
    ]

    name = models.CharField('姓名', max_length=50)
    birth_date = models.CharField('出生年月', max_length=20)
    ethnicity = models.CharField('民族', max_length=20, default='汉族')
    hometown = models.CharField('籍贯', max_length=100)
    political_status = models.CharField(
        '政治面貌', max_length=20, choices=POLITICAL_CHOICES, default='群众'
    )
    grade = models.CharField('年级', max_length=20)
    email = models.EmailField('邮箱', blank=True)
    wechat = models.CharField('微信', max_length=50, blank=True)
    qq = models.CharField('QQ', max_length=20, blank=True)
    photo = models.ImageField('个人照片', upload_to='photos/', blank=True)
    specialties = models.TextField('个人特长', blank=True)
    hobbies = models.TextField('个人爱好', blank=True)
    future_plan = models.TextField('未来10年规划', blank=True)

    # 验证课程 — 用于登录验证
    verify_course = models.CharField(
        '验证课程', max_length=100,
        help_text='用于身份验证的课程名称，用户需输入姓名和此课程才能通过验证'
    )

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '个人简历'
        verbose_name_plural = '个人简历'

    def __str__(self):
        return self.name


class Course(models.Model):
    """所学课程"""
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='courses', verbose_name='所属人员'
    )
    name = models.CharField('课程名称', max_length=100)
    semester = models.CharField('学期', max_length=30, blank=True)

    class Meta:
        verbose_name = '所学课程'
        verbose_name_plural = '所学课程'

    def __str__(self):
        return self.name


class FavoriteWebsite(models.Model):
    """最喜爱的网站链接"""
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='websites', verbose_name='所属人员'
    )
    title = models.CharField('网站名称', max_length=100)
    url = models.URLField('网站地址')
    description = models.CharField('描述', max_length=200, blank=True)

    class Meta:
        verbose_name = '喜爱网站'
        verbose_name_plural = '喜爱网站'

    def __str__(self):
        return self.title
