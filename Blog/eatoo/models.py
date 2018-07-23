from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.
from django.utils import timezone


class EatooUser(AbstractUser):
    """用户表"""
    mobile = models.IntegerField(null=True, blank=True, verbose_name="手机号")
    gender = models.CharField(max_length=10, default="male", verbose_name="性别")
    avatar = models.ImageField(upload_to="uploads/%Y/%m", default="uploads/default.jpg")
    signature = models.CharField(max_length=200, verbose_name="用户签名", default="就知道吃")

    def __str__(self):
        return self.username


class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length=100, verbose_name="文章标题")
    content = RichTextUploadingField(verbose_name="文章详情", null=True, blank=True)
    author = models.ForeignKey("EatooUser", on_delete=models.CASCADE, related_name="articles", verbose_name="文章作者")
    type = models.ForeignKey("Type", on_delete=models.CASCADE, verbose_name="文章类型")
    issuetime = models.DateTimeField(verbose_name="发布日期", default=timezone.now)
    modify_date = models.DateTimeField(verbose_name="最后修改日期", auto_now=True, null=True)
    click_num = models.IntegerField(verbose_name="点击数", null=True, default=0)
    like = models.ForeignKey("EatooUser",on_delete=models.CASCADE, related_name="user_likes", verbose_name="收藏", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-issuetime",)


class Type(models.Model):
    name = models.CharField(max_length=100,verbose_name="分类")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    description = models.CharField(max_length=200, verbose_name="分类描述")

    def __str__(self):
        return self.name


class Comments(models.Model):
    """评论表"""
    content = models.CharField(max_length=500, verbose_name="评论内容", )
    cmt_time = models.DateTimeField(verbose_name="评论发表日期", default=timezone.now)
    # p_comment = models.ForeignKey('Comments', on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="article_comments")
    user = models.ForeignKey("EatooUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name

class Tag(models.Model):
    """标签表"""
    name = models.CharField(max_length=50, verbose_name="标签")
    article = models.ManyToManyField(Article, through="ArticleTag")
    description = models.CharField(max_length=50, verbose_name="标签描述")
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="标签添加时间")


    def __str__(self):
        return self.name



class ArticleTag(models.Model):
    """标签文章关联表"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    data_created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, verbose_name="标签描述")





