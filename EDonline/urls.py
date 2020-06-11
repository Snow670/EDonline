from django.urls import path,include
import xadmin
from django.views.generic import TemplateView
# from users.views import user_login
from users.views import LoginView,Logout_view,RegisterView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'),name='index'),
    # path('login', TemplateView.as_view(template_name='login.html'),name='login'),
    # path('login/',user_login,name='login'),     #修改login路由
    path('logout/',Logout_view,name="logout"),
    path('login/',LoginView.as_view(),name="login"),
    path('register/',RegisterView.as_view(),name="register"),
    path('captcha/',include("captcha.urls")),


]
