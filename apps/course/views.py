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


from operation.models import UserFavorite
class CourseDetailView(View):
    '''课程详情页'''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程的点击数加1
        course.click_nums += 1
        course.save()
        #收藏
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
                if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                    has_fav_org = True

        # 通过当前课程标签，查找数据库中的课程
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:3]
        else:
            relate_courses = []
        context = {
            "course":course,
            "relate_courses":relate_courses,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org

        }
        return render(request,'course/course-detail.html',context)


from .models import CourseResource
class CourseInfoView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        context = {
            "course":course,
            "all_resources":all_resources
        }
        return render(request,'course/course-video.html',context)


from operation.models import CourseComments
class CourseCommentView(View):
    '''课程评论'''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        context = {
            "course":course,
            "all_resources": all_resources,
            "all_comments":all_comments
        }
        return render(request,'course/course-comment.html',context)


from .models import Video
class VideoPlayView(View):
    '''视频播放'''
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        context = {
            "video":video,
            "course":course
        }
        return render(request,'course/course-play.html',context)


from django.http import HttpResponse
class AddCommentView(View):
    '''发表评论'''
    def post(self,request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail","msg":"用户未登录"}')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id)>0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}')