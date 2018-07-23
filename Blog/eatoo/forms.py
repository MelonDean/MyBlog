from django.forms import Widget

from .models import *

from django import forms


class RegisterForm(forms.ModelForm):

    class Meta:
        model = EatooUser
        fields = ['username', 'password', 'email']

        labels = {
            "username": "用户名",
            "password": "密码",
            "email": "邮箱"
        }

        help_texts = {
            "username": "请输入用户名",
            "password": "请输入密码",
            "email": "请输入邮箱",
        }

        widgets = {
            "username": forms.TextInput(attrs={'class': 'form-control','id':'register-username', 'placeholder': '请输入用户名'}),
            "password": forms.PasswordInput(attrs={'class': 'form-control', 'id':'register-password','placeholder': '请输入密码'}),
            "email": forms.TextInput(attrs={"class": 'form-control','id':'register-email', 'placeholder': '请输入邮箱'})
        }

        error_messages = {
            "username": {
                "required": "用户名不能为空",
            },
            "email":{
                "required":"邮箱不能为空",
                "invalid":"邮箱格式有误",
            },
            "password":{
                "required":"密码不能为空",
            }
        }


class ModifyAvatarModelForm(forms.ModelForm):
    class Meta:
        model = EatooUser
        fields = ("avatar",)


class PublishModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "content", "type")




