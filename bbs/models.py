from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from django.contrib.auth.models import User, AbstractUser


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=255)
    # 描述
    brief = models.CharField(null=True, blank=True, max_length=255)
    # on_delete=models.CASCADE：表示级联删除
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    content = models.TextField(u"文章内容")
    author = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    # 时间自动生成
    # auto_now_add:保存第一次创建文章时候的时间，后面修改文章时间不改变
    pub_date = models.DateTimeField(blank=True, null=True)
    # auto_now:后面修改文章的话时间改变
    last_modify = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(u"优先级", default=1000)
    # upload_to：将图片文件存储到./uploads目录下，default未没有设置图片时的默认路径（有问题，访问路径总是/static/uploads/default.jpg，访问不到图片）
    # default写什么，数据库中存储路径就是什么
    head_img = models.ImageField(u"文章标题图片", upload_to="./uploads", default="uploads/default.jpg")
    users_liked = models.IntegerField(u"点赞数", default=0)
    users_thumb = models.CharField(max_length=255)
    status_choices = (
        ("draft", u"草稿"),
        ("published", u"已发布"),
        ("hidden", u"隐藏")
    )
    status = models.CharField(choices=status_choices, default="published", max_length=255)

    def clean(self):
        if self.status == "draft" and self.pub_date is not None:
            raise ValidationError("Draft entries may not have a publication date.")
        if self.status == "published" and self.pub_date is None:
            self.pub_date = datetime.date.today()

    # def __str__(self):
    #     return 'title': self.title, 'users_thumb':self.users_thumb, 'users_liked'self.users_liked


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name=u"所属文章", on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", related_name="my_children", blank=True, null=True,
                                       on_delete=models.CASCADE)
    comment_choices = ((1, u"评论"),
                       (2, u"点赞"))
    comment_type = models.IntegerField(choices=comment_choices, default=1)
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def clean(self):
        if self.comment_type == 1 and len(self.comment) == 0:
            raise ValidationError("评论内容不能为空")

    def __str__(self):
        return "C:%s" % self.comment


class Category(models.Model):
    name = models.CharField(max_length=255)
    # blank：针对表单而言，若为True，表示表单填写该字段时可以不填
    # null：针对数据库而言，若为True, 表示数据表中该字段可以为空
    brief = models.CharField(null=True, blank=True, max_length=255)
    # 板块动态展示
    set_as_top_menu = models.BooleanField(default=False)
    position_index = models.SmallIntegerField()
    # 板主
    admins = models.ManyToManyField("UserProfile", blank=True)

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 昵称
    username = models.CharField(max_length=255)
    signature = models.CharField(max_length=255, blank=True, null=True)
    # 图片尺寸出了问题？？？
    # 去掉height_field=150, width_field=150, 这两个参数，就不会报错了，原因查看https://blog.csdn.net/guothree2003/article/details/96477788
    head_img = models.ImageField(u"头像", upload_to="media", default="media/default.jpg", blank=True, null=True)

    def __str__(self):
        return self.username

class CodeEditor(models.Model): # 代码编译器
    # 编程语言
    language = models.CharField(max_length=20)
    # 代码区域
    code = models.CharField(max_length=255, blank=True, null=True)

class Problem(models.Model): # 问题
    # 题号
    problem_number = models.CharField(max_length=255, blank=True, null=True)

    problem_title = models.CharField(max_length=255, blank=True, null=True)
    # 问题描述
    problem_description = models.CharField(max_length=255, blank=True, null=True)
    # 输入格式
    input_style = models.CharField(max_length=255, blank=True, null=True)
    # 输出格式
    output_style = models.CharField(max_length=255, blank=True, null=True)
    # 数据范围
    data_range = models.CharField(max_length=255, blank=True, null=True)
    # 样例输入
    input_sample = models.CharField(max_length=255, blank=True, null=True)
    # 样例输出
    output_sample = models.CharField(max_length=255, blank=True, null=True)
    # 难度
    problem_degree = models.CharField(max_length=255, blank=True, null=True)
    # 时间限制/ms
    time_limit = models.IntegerField(blank=True, null=True)
    # 空间限制/k
    space_limit = models.IntegerField(blank=True, null=True)
    # 输入
    input = models.FileField(upload_to=('problem_judge_data\\'))
    #输出
    output = models.FileField(upload_to=('problem_judge_data\\'))