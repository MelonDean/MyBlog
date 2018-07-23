from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(EatooUser)
class EatooUserAdmin(admin.ModelAdmin):
    list_display = ['mobile', 'username', 'gender', 'signature']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'ctime', 'description']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'issuetime', 'content','type','modify_date']


    class Media():
        js = (
            '/static/js/kindeditor/kindeditor-all.js',
            '/static/js/kindeditor/kindeditor-all-min.js',
            '/static/js/kindeditor/config.js',
        )


@admin.register(Comments)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['content', 'cmt_time', 'article', 'user']


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['name','description','ctime']


