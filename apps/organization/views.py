from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger

from .models import CourseOrg,CityDict

# Create your views here.


class OrgView(View):
    ''' 课程机构'''
    def get(self,request):
        all_orgs = CourseOrg.objects.all()      # 所有机构
        all_citys = CityDict.objects.all()      # 所有城市

        hot_orgs = all_orgs.order_by('-click_nums')[:3]      #获取所有机构点击数

        city_id = request.GET.get('city','')       #获取前端传递的city.id
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get('ct','')        #获取前端传递的机构分类
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()             # 有多少家机构

        sort = request.GET.get('sort','')          #根据学习人数和课程数进行排名
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 对课程机构进行分页,尝试获取前台get请求传递过来的page参数
        paginator = Paginator(all_orgs, 3, request=request)
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1                            # 如果是不合法的配置参数默认返回第一页
        page_orgs_dict = paginator.page(page)

        context = {
            "all_orgs":page_orgs_dict,
            "org_nums":org_nums,
            "all_citys":all_citys,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort
        }
        return render(request,'organization/org-list.html',context)


from .forms import UserAskForm
from django.http import HttpResponse

class AddUserAskView(View):
    '''添加用户咨询'''
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # user_ask = UserAsk()
            # user_ask.name = request.POST.get('name')
            # user_ask.mobile = request.POST.get('mobile')
            # user_ask.course_name = request.POST.get('course_name')
            # user_ask.save()
            userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}')


class OrgHomeView(View):
    '''机构首页'''
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 反向查询到课程机构的所有课程和老师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        context = {
            "course_org":course_org,
            "all_courses":all_courses,
            "all_teacher":all_teacher,
            "current_page":current_page,
            "has_fav":has_fav
        }
        return render(request,'organization/org-detail-homepage.html',context)


class OrgCourseView(View):
    '''机构课程'''
    def get(self,request,org_id):
        current_page = 'couser'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        context = {
            "all_courses":all_courses,
            "course_org":course_org,
            "current_page": current_page,
            "has_fav": has_fav
        }
        return render(request,'organization/org-detail-course.html',context)


class OrgDescView(View):
    '''机构介绍'''
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        context = {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav
        }
        return render(request,'organization/org-detail-desc.html',context)


class OrgTeacherView(View):
    '''机构讲师'''
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        context = {
            "course_org": course_org,
            "all_teacher":all_teacher,
            "current_page": current_page,
            "has_fav": has_fav
        }
        return render(request,'organization/org-detail-teachers.html',context)


from operation.models import UserFavorite
class AddFavView(View):
    '''收藏和取消收藏'''
    def post(self,request):
        id = request.POST.get('fav_id',0)
        type = request.POST.get("fav_type",0)

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail"}')
        record = UserFavorite.objects.filter(user=request.user,fav_id=int(id),fav_type=int(type))
        if record:
            record.delete()
            return HttpResponse('{"status":"success", "msg":"已取消收藏"}')
        else:
            user_fav = UserFavorite()
            if int(id)>0 and int(type)>0:
                user_fav.user = request.user
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}')





