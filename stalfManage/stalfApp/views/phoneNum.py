from django.shortcuts import render, HttpResponse, redirect
from stalfApp import models
from stalfApp.models import PrettyNum
from django.utils.safestring import mark_safe
from stalfApp.utils.pagination import Pagination

import copy
#from django.http.request import QueryDict

from stalfApp.utils.form import PhoneNumMobelFrom


def phoneNum_list(request):
    # 在搜索基础上保留进行换页
    query_dict = copy.deepcopy(request.GET)
    # print(type(query_dict))
    query_dict._mutable = True
    # query_dict.setlist('page', [2])
    # print(query_dict.urlencode())

    # 搜索查询
    # test1 = PrettyNum.objects.filter(phoneNum="17527773195",id=1).first()
    # print(test1.phoneNum, test1.get_level_display())
    # #通过字典查找
    # dis = {"phoneNum":"17527773195","id":1}
    # test2 = PrettyNum.objects.filter(**dis).first()
    # print(test2.phoneNum, test2.get_level_display())

    # 查找
    # 对于数字
    # test3=PrettyNum.objects.filter(id=2)   #等于2
    # test3 = PrettyNum.objects.filter(id__gt=2)  # 大于2
    # test3 = PrettyNum.objects.filter(id__gte=2)  # 大于等于2
    # test3 = PrettyNum.objects.filter(id__lt=2)  # 小于2
    # test3 = PrettyNum.objects.filter(id__lte=2)  # 小于等于2
    # 针对字符串
    # test3=PrettyNum.objects.filter(phoneNum__startswith="175")  #以XXX开头
    # test3=PrettyNum.objects.filter(phoneNum__endswith="175")    #以XXX结尾
    # test3=PrettyNum.objects.filter(phoneNum__contains="175")    #包含XXX

    dis_dict = {}
    search_data = request.GET.get('key', "")
    if search_data:
        dis_dict["phoneNum__contains"] = search_data

    # res = PrettyNum.objects.filter(**dis_dict)
    # print(res)

    page_object = Pagination(request)
    # 分页操作
    page = int(request.GET.get('page', 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size

    # 页码
    # 获取总页码数
    total_count = PrettyNum.objects.filter(**dis_dict).order_by("-level").count()
    # divmod(x, y)-->返回(商，余数）
    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1

    # 计算当前页前后页
    plus = 5
    # 数据较少
    if total_page_count <= 2 * plus + 1:
        start_page = 1
        end_page = total_page_count
    else:
        # 数据过多
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            # 当前页面+5大于total
            if (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus

    page_str_list = []
    # 上一页
    if page > 1:
        query_dict.setlist('page', [page - 1])
        prev = '<li><a href="?page={}">上一页</a></li>'.format(query_dict.urlencode())
    else:
        query_dict.setlist('page', [1])
        prev = '<li><a href="?{}">上一页</a></li>'.format(query_dict.urlencode())
    page_str_list.append(prev)

    # range前取后不取
    for i in range(1, total_page_count + 1):
        query_dict.setlist('page', [i])
        if i == page:
            ele = '<li class="active" ><a href="?{}">{}</a></li>'.format(query_dict.urlencode(), i)
        ele = '<li><a href="?{}">{}</a></li>'.format(query_dict.urlencode(), i)
        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        query_dict.setlist('page', [page + 1])
        prev = '<li><a href="?{}">下一页</a></li>'.format(query_dict.urlencode())
    else:
        query_dict.setlist('page', [total_page_count])
        prev = '<li><a href="?{}">下一页</a></li>'.format(query_dict.urlencode())
    page_str_list.append(prev)

    page_string = mark_safe("".join(page_str_list))

    # 数据库获取数据
    # 排序，添加负号表示倒序，即大的数据在前面
    # data_list = PrettyNum.objects.all().order_by("-level")
    data_list = PrettyNum.objects.filter(**dis_dict).order_by("-level")[page_object.start:page_object.end]

    return render(request,
                  'phoneNum_list.html',
                  {'data_list': data_list, "search_data": search_data, "page_string": page_string})


def phoneNum_add(request):
    if (request.method == "GET"):
        form = PhoneNumMobelFrom()

        return render(request, 'phoneNum_add.html', {'form': form})

    # 获取用户提交数据
    form = PhoneNumMobelFrom(data=request.POST)
    if form.is_valid():
        # 获取数据合法，保存至数据库
        form.save()
        return redirect("/phoneNum/list/")
    else:
        return render(request, 'phoneNum_add.html', {'form': form})


def phoneNum_edit(request, nid):
    # 获取对应数据
    row_object = PrettyNum.objects.filter(id=nid).first()

    if (request.method == "GET"):
        # 将数据添加到初始form中
        form = PhoneNumMobelFrom(instance=row_object)
        return render(request, 'phoneNum_edit.html', {'form': form})

    # 获取用户输入信息
    form = PhoneNumMobelFrom(data=request.POST, instance=row_object)
    # 进行校验
    if form.is_valid():
        form.save()

        return redirect("/phoneNum/list")
    else:
        return render(request, 'phoneNum_edit.html', {'form': form})


def phoneNum_delete(request, nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect('/phoneNum/list')

