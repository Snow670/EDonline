from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger

from .models import Course


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,3 , request=request)
        courses = p.page(page)
        context = {
           "all_courses":courses,
           "hot_courses":hot_courses,
           "sort":sort
           }
        return render(request,'course/course-list.html',context)


class CourseDetailView(View):
    '''课程详情页'''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程的点击数加1
        course.click_nums += 1
        course.save()
        # 通过当前课程标签，查找数据库中的课程
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:3]
        else:
            relate_courses = []
        context = {
            "course":course,
            "relate_courses":relate_courses
        }
        return render(request,'course/course-detail.html',context)