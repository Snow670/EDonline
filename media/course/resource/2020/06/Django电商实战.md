## （一）、后台管理模板Xadmin使用

1. 参考网站：http://x.xuebingsi.com/

2. 创建项目：安装依赖

   django=2.2.5     

   django-admin startproject unicom

   python manage.py startapp  unicomapp

3. 数据库

   ```python
   class User(models.Model):
       name = models.CharField(max_length=100)
       email = models.EmailField()
       message = models.CharField(max_length=300)
       create_at = models.DateTimeField(auto_now_add=True)  
   ```

   安装数据库驱动：python3 中  mysqlclient

   ```
   pip install mysqlclient
   pip install pymysql
   ```

   配置数据库

   ```
   import pymysql
   pymysql.install_as_MySQLdb()
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME':'unicom_db',
           'USER':'root',
           'PASSWORD':'123456',
           'HOST':'127.0.0.1',
           'PORT':'3306'
       }
   }
   ```

   设置本地化

   ```
   # 设置语言为中文
   LANGUAGE_CODE = 'zh-hans'
   # 时区改为上海
   TIME_ZONE = 'Asia/Shanghai'
   ```

   同步数据库

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

   报错

   ```
   第一个错  raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
   django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.
   
   
   打开base.py  将35,36行注释
   
   第二个错  File "C:\Users\Bruce\Desktop\root\unicom\env\lib\site-packages\django\db\backends\mysql\operations.py", line 146, in last_executed_query     AttributeError: 'str' object has no attribute 'decode'
   operations.py第146行改为：  query = query.encode(errors='replace')
   ```

   

4. xadmin

   - 安装xadmin：pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2

   - 注册app   

     ```
     ‘xadmin’，
     'crispy_forms',
     'reversion',
     ```

   - 注册urls

     ```python
     from django.urls import path,include
     import xadmin
     
     urlpatterns = [
         path('xadmin/',xadmin.site.urls)
     ]
     ```

4. 创建unicomapp对应的admin（adminx.py）

   ```python
   import xadmin
   from xadmin import views
   from .models import User
   
   class BaseSetting(object):
       '''
       xadmin的基础配置
       '''
       enable_themes = True # 开启主题功能
       use_bootswatch = True
   
   class GlobalSettings(object):
       '''
           设置网站标题和页脚
       '''
       site_title = "中国联通后台管理页面"
       site_footer = "Powered By 1903C - 2020"
   
   xadmin.site.register(views.BaseAdminView,BaseSetting)
   xadmin.site.register(views.CommAdminView,GlobalSettings)
   
   class UserAdmin(object):
       '''
           后台展示的内容
           后台可以搜索的内容
           后台过滤器可以使用的内容
       '''
       list_display = ['name','email','message']
       search_fields = ['name','email','message']
       list_filter = ['name','email','message','create_at']
   
   xadmin.site.register(User,UserAdmin)
   ```

   

## （二）、使用的Xadmin在线教育网站后台

#### 一、环境安装

1. Python == 3.7  
2. Django == 2.2
3. xadmin == 2.01

#### 二、创建项目

1. django-admin startproject bwOnline

2. 连接数据库，见（一）中

3. 指定静态路径 static文件夹

4. 创建4个app：users，course，organization，operation，并注册

5. 创建一个apps文件夹，将这4个app拖入apps中，

6. 将apps目录添加到项目路径中

   ```
   import os
   import sys
   # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   sys.path.insert(0,os.path.join(BASE_DIR,'apps'))
   ```

7. 使用自己写的UserProfile

   ```
   AUTH_USER_MODEL = 'users.UserProfile'
   ```

   

#### 三、数据库设计

1. **users  models.py**

```mysql
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    # 自定义的性别选择规则
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    # 昵称
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    # 生日，可以为空
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    # 性别 只能男或女，默认女
    gender = models.CharField(
        max_length=6,
        verbose_name=u"性别",
        choices=GENDER_CHOICES,
        default="female")
    # 地址
    address = models.CharField(max_length=100, verbose_name="地址", default="")
    # 电话
    mobile = models.CharField(max_length=11, null=True, blank=True)
    # 头像 默认使用default.png  需要pillow，所以安装pillow
    image = models.ImageField(
        upload_to="image/%Y/%m",
        default=u"image/default.png",
        max_length=100
    )

    # meta信息，即后台栏目名
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # 重载str方法，打印实例会打印username，username为继承自abstractuser
    def __str__(self):
        return self.username


# 邮箱验证码model
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ("register", u"注册"),
        ("forget", u"找回密码")
    )
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    # 未设置null = true blank = true 默认不可为空
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=SEND_CHOICES, max_length=10)
    # 这里的now得去掉(),不去掉会根据编译时间。而不是根据实例化时间。
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name


# 轮播图model
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(
        upload_to="banner/%Y/%m",
        verbose_name=u"轮播图",
        max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    # 默认index很大靠后。想要靠前修改index值。
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

```

其余操作参考（一）

2. course   models.py

   ```mysql
   from datetime import datetime
   
   # 课程信息表
   from django.db import models
   
   
   class Course(models.Model):
       DEGREE_CHOICES = (
           ("cj", u"初级"),
           ("zj", u"中级"),
           ("gj", u"高级")
       )
       name = models.CharField(max_length=50, verbose_name=u"课程名")
       desc = models.CharField(max_length=300, verbose_name=u"课程描述")
       # TextField允许我们不输入长度。可以输入到无限大。暂时定义为TextFiled，之后更新为富文本
       detail = models.TextField(verbose_name=u"课程详情")
       degree = models.CharField(choices=DEGREE_CHOICES, max_length=2)
       # 使用分钟做后台记录(存储最小单位)前台转换
       learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
       # 保存学习人数:点击开始学习才算
       students = models.IntegerField(default=0, verbose_name=u"学习人数")
       fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
       image = models.ImageField(
           upload_to="courses/%Y/%m",
           verbose_name=u"封面图",
           max_length=100)
       # 保存点击量，点进页面就算
       click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"课程"
           verbose_name_plural = verbose_name
   
   
   # 章节
   class Lesson(models.Model):
       # 因为一个课程对应很多章节。所以在章节表中将课程设置为外键。
       # 作为一个字段来让我们可以知道这个章节对应那个课程
       course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
       name = models.CharField(max_length=100, verbose_name=u"章节名")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"章节"
           verbose_name_plural = verbose_name
   
   
   # 每章视频
   class Video(models.Model):
       # 因为一个章节对应很多视频。所以在视频表中将章节设置为外键。
       # 作为一个字段来存储让我们可以知道这个视频对应哪个章节.
       lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)
       name = models.CharField(max_length=100, verbose_name=u"视频名")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"视频"
           verbose_name_plural = verbose_name
   
   
   # 课程资源
   class CourseResource(models.Model):
       # 因为一个课程对应很多资源。所以在课程资源表中将课程设置为外键。
       # 作为一个字段来让我们可以知道这个资源对应那个课程
       course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
       name = models.CharField(max_length=100, verbose_name=u"名称")
       # 这里定义成文件类型的field，后台管理系统中会直接有上传的按钮。
       # FileField也是一个字符串类型，要指定最大长度。
       download = models.FileField(
           upload_to="course/resource/%Y/%m",
           verbose_name=u"资源文件",
           max_length=100)
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"课程资源"
           verbose_name_plural = verbose_name
   
   ```

   

3. **organization  models.py**

   ```mysql
   from datetime import datetime
   
   from django.db import models
   
   # Create your models here.
   
   
   # 城市字典
   class CityDict(models.Model):
       name = models.CharField(max_length=20, verbose_name=u"城市")
       # 城市描述：备用不一定展示出来
       desc = models.CharField(max_length=200, verbose_name=u"描述")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"城市"
           verbose_name_plural = verbose_name
   
   
   # 课程机构
   class CourseOrg(models.Model):
       name = models.CharField(max_length=50, verbose_name=u"机构名称")
       # 机构描述，后面会替换为富文本展示
       desc = models.TextField(verbose_name=u"机构描述")
       click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
       fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
       image = models.ImageField(
           upload_to="org/%Y/%m",
           verbose_name=u"封面图",
           max_length=100)
       address = models.CharField(max_length=150, verbose_name=u"机构地址")
       # 一个城市可以有很多课程机构，通过将city设置外键，变成课程机构的一个字段
       # 可以让我们通过机构找到城市
       city = models.ForeignKey(CityDict, verbose_name=u"所在城市", on_delete=models.CASCADE)
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"课程机构"
           verbose_name_plural = verbose_name
   
   
   # 讲师
   class Teacher(models.Model):
       # 一个机构会有很多老师，所以我们在讲师表添加外键并把课程机构名称保存下来
       # 可以使我们通过讲师找到对应的机构
       org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", on_delete=models.CASCADE)
       name = models.CharField(max_length=50, verbose_name=u"教师名称")
       work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
       work_company = models.CharField(max_length=50, verbose_name=u"就职公司")
       work_position = models.CharField(max_length=50, verbose_name=u"公司职位")
       points = models.CharField(max_length=50, verbose_name=u"教学特点")
       click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
       fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"教师"
           verbose_name_plural = verbose_name
   
   ```

   

4. operation  models.py

   ```mysql
   from datetime import datetime
   
   # 引入我们CourseComments所需要的外键models
   from django.db import models
   
   from users.models import UserProfile
   from course.models import Course
   
   # 用户我要学习表单
   class UserAsk(models.Model):
       name = models.CharField(max_length=20, verbose_name=u"姓名")
       mobile = models.CharField(max_length=11, verbose_name=u"手机")
       course_name = models.CharField(max_length=50, verbose_name=u"课程名")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"用户咨询"
           verbose_name_plural = verbose_name
   
   
   # 用户对于课程评论
   class CourseComments(models.Model):
   
       # 会涉及两个外键: 1. 用户， 2. 课程。import进来
       course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
       user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
       comments = models.CharField(max_length=250, verbose_name=u"评论")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"评论时间")
   
       class Meta:
           verbose_name = u"课程评论"
           verbose_name_plural = verbose_name
   
   
   # 用户对于课程,机构，讲师的收藏
   class UserFavorite(models.Model):
       # 会涉及四个外键。用户，课程，机构，讲师import
       TYPE_CHOICES = (
           (1, u"课程"),
           (2, u"课程机构"),
           (3, u"讲师")
       )
   
       user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
       # course = models.ForeignKey(Course, verbose_name=u"课程")
       # teacher = models.ForeignKey()
       # org = models.ForeignKey()
       # fav_type =
   
       # 机智版
       # 直接保存用户的id.
       fav_id = models.IntegerField(default=0)
       # 表明收藏的是哪种类型。
       fav_type = models.IntegerField(
           choices=TYPE_CHOICES,
           default=1,
           verbose_name=u"收藏类型")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"评论时间")
   
       class Meta:
           verbose_name = u"用户收藏"
           verbose_name_plural = verbose_name
   
   
   # 用户消息表
   class UserMessage(models.Model):
           # 因为我们的消息有两种:发给全员和发给某一个用户。
           # 所以如果使用外键，每个消息会对应要有用户。很难实现全员消息。
   
           # 机智版 为0发给所有用户，不为0就是发给用户的id
       user = models.IntegerField(default=0, verbose_name=u"接收用户")
       message = models.CharField(max_length=500, verbose_name=u"消息内容")
   
       # 是否已读: 布尔类型 BooleanField False未读,True表示已读
       has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"用户消息"
           verbose_name_plural = verbose_name
   
   
   # 用户课程表
   class UserCourse(models.Model):
       # 会涉及两个外键: 1. 用户， 2. 课程。import进来
       course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
       user = models.ForeignKey(UserProfile, verbose_name=u"用户", on_delete=models.CASCADE)
       add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
   
       class Meta:
           verbose_name = u"用户课程"
           verbose_name_plural = verbose_name
   
   ```

   

5. 同步所有数据库操作

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

   

#### 四、xadmin简单配置

1. 导航英文修改为中文

   ```python
   每个app中的apps.py
   
   from django.apps import AppConfig
   
   
   class UsersConfig(AppConfig):
       name = 'users'
       verbose_name = '用户信息'
   
   ```

   

2. 修改每个app中的`__init__.py`

   ```
   default_app_config = 'users.apps.UsersConfig'
   ```

   





## 三、







