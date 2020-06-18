from django.urls import path,include,re_path
import xadmin
from django.views.static import serve
from EDonline.settings import MEDIA_ROOT

from django.views.generic import TemplateView
# from users.views import user_login
from users.views import LoginView,Logout_view,RegisterView,ActiveUserView,ForgetPwdView,ResetPwdView,ModifyPwdView



urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'),name='index'),
    # path('login', TemplateView.as_view(template_name='login.html'),name='login'),
    # path('login/',user_login,name='login'),     #修改login路由
    path('logout/',Logout_view,name="logout"),
    path('login/',LoginView.as_view(),name="login"),
    path('register/',RegisterView.as_view(),name="register"),
    path('captcha/',include("captcha.urls")),
    re_path('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active'),
    path('forget/',ForgetPwdView.as_view(),name='forget'),
    re_path('reset/(?P<active_code>.*)/', ResetPwdView.as_view(), name='reset_pwd'),
    path('modify/', ModifyPwdView.as_view(), name='modify_pwd'),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    path("org/", include('organization.urls', namespace="org")),
    path("course/", include('course.urls', namespace="course")),
    path("users/", include('users.urls', namespace="users")),

]
