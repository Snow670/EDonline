from django import forms
from captcha.fields import CaptchaField

# 登录表单验证
class LoginForm(forms.Form):
    #用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)


#注册的表单验证
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6)
    captcha = CaptchaField()