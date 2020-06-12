from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile

# Create your views here.

# @csrf_exempt
# def user_users/login(request):
#     # if request.is_ajax():
#     response = HttpResponse('test',content_type='application/json')
#     data = request.body
#     res = data.decode('utf-8')
#     res = json.loads(res)
#     username = res['username']
#     password = res['password']
#     print(username,password)
#     #调用authenticate校检用户名和密码
#     user = authenticate(username=username, password=password)
#     response.set_cookie("username",user.username,60*60*24*15)
#     response.set_cookie("password",user.password,60*60*24*15)
#     request.COOKIES.get('username')
#     response["Access-Control-Allow-Credentials"] = "true"
#     response["Access-Control-Allow-Origin"] = "http://localhost:8000"
#     # 如果不是null说明验证成功
#     if user is not None:
#         # 登录
#         users/login(request, user)
#         resp = {"status":"success"}
#         return JsonResponse(resp)
#         # return HttpResponse(json.dumps(resp),content_type='application/json')
#     else:
#         resp = {"status":"fail"}
#         return JsonResponse(resp)
#         # return HttpResponse(json.dumps(resp),content_type='application/json')

#上传文件
# def upload(request):
#     if request.method == "POST":
#         file_obj = request.FILES.get('file')
#         with open(file_obj.name,"wb") as f:
#             for chuck in file_obj.chunks():
#               f.write()
#         return JsonResponse(resp)

# def user_users/login(request):
#     if request.method == 'POST':
#         # 获取用户提交的用户名和密码
#         user_name = request.POST.get('username', None)
#         pass_word = request.POST.get('password', None)
#         # 成功返回user对象,失败None
#         #调用authenticate校检用户名和密码
#         user = authenticate(username=user_name, password=pass_word)
#         # 如果不是null说明验证成功
#         if user is not None:
#             # 登录
#             users/login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'users/login.html', {'msg': '用户名或密码错误'})
#
#     elif request.method == 'GET':
#         return render(request, 'users/login.html')

#登出
def Logout_view(request):
    logout(request)
    return render(request,'users/login.html')

#Ajax 的登出
# def Logout_view(request):
#     response = HttpResponse('退出')
#     #删除cookie
#     response.delete_cookie('password')
#     logout(request)
#     return response

#邮箱和用户名，手机号都可以登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

from django.views.generic.base import View
from .forms import LoginForm

class LoginView(View):
    def get(self,request):
        return render(request,'users/login.html')

    def post(self,request):
        #实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    #只有注册激活才能登录
                    login(request,user)
                    return render(request,'index.html')
                else:
                    return render(request, 'users/login.html', {"msg": "用户名或密码错误", "login_form": login_form})
            else:
                return render(request,'users/login.html',{"msg":"用户名或密码错误","login_form":login_form})

        else:
            return render(request,"users/login.html",{"login_form":login_form})


'''
    邮箱注册
'''
from .forms import RegisterForm
from utils.email_send import send_register_email


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'users/register.html',{"register_form":register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email")
            if UserProfile.objects.filter(email=username):
                return render(request,'users/register.html',{"register_form":register_form,"msg":"用户已存在"})
            password = request.POST.get('password')
            #实例化一个UserProfile对象，存储到数据库
            user = UserProfile()
            user.username = username
            # 对保存到数据库的密码加密
            user.password = make_password(password)
            user.email = username
            user.is_active = False
            user.save()

            #发送激活的邮件,python中有一个SMPT模块，django与之对应的django.core.mail
            send_register_email(username,"register")
            return render(request,'users/login.html')
        else:
            return render(request,'users/register.html')


'''
    处理激活账户的视图
'''
from .models import EmailVerifyRecord


class ActiveUserView(View):
    def get(self,request,active_code):

        #检查邮箱验证记录中数据表中是否存在active_code
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'users/active_fail.html')
        return render(request,'users/login.html')


'''
    发送重置密码的链接
'''
from .forms import ForgetForm


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'users/forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email',None)
            send_register_email(email,'forget')
            return render(request, 'users/send_success.html')
        else:
            return render(request,'users/forgetpwd.html',{'forget_form':forget_form})


'''
    重置密码的视图
'''

class ResetPwdView(View):

    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "users/password_reset.html", {"email": email})
        else:
            return render(request, "users/active_fail.html")
        return render(request, "users/login.html")


'''
    修改密码
'''
from .forms import ModifyForm


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1")
            pwd2 = request.POST.get("password2")
            email = request.POST.get("email")
            if pwd1 != pwd2:
                return render(request, "users/password_reset.html", {"email":email, "msg":"密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "users/login.html")
        else:
            email = request.POST.get("email")
            return render(request, "users/password_reset.html", {"email":email, "modify_form":modify_form })