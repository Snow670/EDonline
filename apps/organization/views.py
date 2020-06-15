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

        city_id = request.GET.get('city','')       #获取前端传递的city.id
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        category = request.GET.get('ct','')        #获取前端传递的机构分类
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_nums = all_orgs.count()             # 有多少家机构

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
            "category":category
        }
        return render(request,'organization/org-list.html',context)