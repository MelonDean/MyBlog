import json

import os

import re
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,logout

# Create your views here.
from django.urls import reverse
from django.views import View

from eatoo.forms import ModifyAvatarModelForm, PublishModelForm, Comments
from eatoo.models import Article, Tag, EatooUser, Type


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = EatooUser.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        page = request.GET.get("page",1)
        obj = Article.objects.all()
        article_paged = Paginator(obj,3)
        tags = Tag.objects.all()
        articles = article_paged.get_page(page)
        total_page = range(article_paged.num_pages)
        labelcolor = ['default','primary', 'info','success','warning','danger']
        return render(request, 'index.html', locals())


class ArticleView(View):
    def get(self,request,article_id):
        articles = Article.objects.all()
        tags = Tag.objects.all()
        labelcolor = ['default', 'primary', 'info', 'success', 'warning', 'danger']
        article_detail = Article.objects.get(pk=article_id)
        Article.objects.filter(pk=article_id).update(click_num =F("click_num")+1)
        return render(request, "article_detail.html", locals())


class LoginView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'login.html')

    def post(self,request):
        username = request.POST.get("login-username")
        password = request.POST.get("login-password")

        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            articles = Article.objects.all()
            tags = Tag.objects.all()
            labelcolor = ['default', 'primary', 'info', 'success', 'warning', 'danger']
            return render(request, 'index.html', locals())
        else:
            modal_content = "账号或者密码错误"
            modal_title = "登陆失败"
            origin_remote = request.path_info
            return render(request, "dialog.html", locals())



class LogoutView(View):
    def get(self, request):
        user = request.user
        logout(request)
        return render(request, 'login.html')


class RegisterView(View):
    def get(self,request):
        from .forms import RegisterForm
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        from .forms import RegisterForm
        register_form = RegisterForm()
        forminfo = RegisterForm(request.POST)
        if forminfo.is_valid():
            username = forminfo.cleaned_data.get("username","")
            password = forminfo.cleaned_data.get("password","")
            email = forminfo.cleaned_data.get("email","")

            eatoouser = EatooUser()
            eatoouser.username = username
            eatoouser.password = make_password(password)
            eatoouser.email = email

            eatoouser.save()
            return redirect(reverse("login"))
        else:
            errors = forminfo.errors
            return render(request, 'register.html', locals())


class UserInfoView(View):
    def get(self,request,userinfo_id):
        return render(request, "userinfo.html", locals())


class ModifyAvatarView(View):
    def post(self,request,avatarid):
        modify_data = ModifyAvatarModelForm(request.POST, request.FILES, instance=request.user)
        if modify_data.is_valid():
            modify_data.save()
        else:
            print(modify_data.errors)
        return render(request, "userinfo.html", {"msg":"修改成功"})

class PublishView(View):
    def get(self,request):
        myarticlelist = request.user.articles.all()
        types = Type.objects.all()
        article_content = PublishModelForm()
        if types and article_content:
            return render(request, "publish_page.html", locals())
        return render(request,"myarticlelist.html", locals() )

    def post(self,request):
        myarticlelist = request.user.articles.all()
        article_content = PublishModelForm(request.POST)
        if article_content.is_valid():
            title = request.POST.get("title")
            content = request.POST.get("content")
            type = request.POST.get("type")
            Article.objects.create(title=title, content=content, type=Type.objects.get(pk=1),author_id=request.user.id)
            return render(request,'myarticlelist.html',locals())
        return render(request, "myarticlelist.html",locals())


class MyArticleListView(View):
    def get(self,request):
        myarticlelist = request.user.articles.all()
        return render(request, 'myarticlelist.html', locals())


class EditArticleView(View):
    def get(self,request,article_id):
        article = Article.objects.get(id=int(article_id))
        return render(request, "article_edit_page.html", locals())

    def post(self,request,article_id):
        myarticlelist = request.user.articles.all()
        article_content = PublishModelForm(request.POST)
        if article_content.is_valid():
            title = request.POST.get("title")
            content = request.POST.get("content")
            type = request.POST.get("type")
            Article.objects.filter(id=article_id).update(title=title, content=content,type=Type.objects.get(pk=type))
            return render(request,'myarticlelist.html',locals())
        return render(request, "publish_page.html")



class DeleteArticleView(View):
    def get(self,request, article_id):
        myarticlelist = request.user.articles.all()
        article = Article.objects.get(id=int(article_id))
        article.delete()
        return render(request, "myarticlelist.html",locals())


class CommentView(View):
    def get(self, request):
        pass

    def post(self, request, article_id):
        print(1)
        # 获取评论双方的信息以及评论内容
        article = Article.objects.get(id=article_id)
        comment_content = request.POST.get("content")
        print(article_id,comment_content)

        Comments.objects.create(article_id=article_id, user_id=request.user.pk, content=comment_content)
        return redirect("/")


