from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger

from .models import CourseOrg,CityDict

# Create your views here.


class OrgView(View):
    '''
    课程机构
    '''
    def get(self,request):
        # 所有课程机构
        all_orgs = CourseOrg.objects.all()
        # 有多少家机构
        org_nums = all_orgs.count()
        # 所有城市
        all_citys = CityDict.objects.all()

        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        paginator = Paginator(all_orgs, 3, request=request)
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        # page_orgs = paginator.page(page).object_list    #object_list分页之后的数据列表
        page_orgs_dict = paginator.page(page)

        context = {
            "all_orgs":page_orgs_dict,
            "org_nums":org_nums,
            "all_citys":all_citys,
        }
        return render(request,'organization/org-list.html',context)