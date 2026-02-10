from django.shortcuts import render, HttpResponse, redirect
from stalfApp import models
from stalfApp.models import Department, UserInfo

import copy
#from django.http.request import QueryDict

from stalfApp.utils.form import UserModelForm
from stalfApp.utils.form import PhoneNumMobelFrom

# Create your views here.


def orm(request):

    #获取数据库所有用户信息
    # data_list = UserInfo.objects.all()
    # print(data_list)

    return HttpResponse("登录成功！")



#用户管理 用户列表
def user_list(request):
    #获取数据库数据
    user_list = UserInfo.objects.all()
    #python语法获取特殊格式的值
    # for obj in user_list:
    #     print(obj.gender, obj.get_gender_display(), obj.creat_time.strftime("%Y-%m-%d"),obj.depart,obj.depart.title)


    return render(request,'user_list.html',{'user_list':user_list})

#添加用户
def user_add(request):
    if(request.method == "GET"):
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list':Department.objects.all()
        }
        return render(request,
                      'user_add.html',
                      context)

    #获取数据
    name = request.POST.get('name')
    pwd = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    creat_time = request.POST.get('creat_time')
    gender = request.POST.get('gender')
    depart = request.POST.get('depart')

    UserInfo.objects.create(name=name,password=pwd,age=age,account=account,creat_time=creat_time,gender=gender,depart_id=depart)

    return redirect("/user/list/")






def modelform_add(request):
    if(request.method == "GET"):
        form = UserModelForm()
        return render(request,'modelform_add.html',{'form':form})

    #获取用户提交数据
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        #获取数据合法，保存至数据库
        form.save()
        return redirect("/user/list/")
    else:
        return render(request,'modelform_add.html',{'form':form})



#编辑用户
def user_edit(request, nid):
    # 根据ID获取对象
    row_object = UserInfo.objects.filter(id=nid).first()
    if(request.method == "GET"):
        form = UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{'form':form})


    form = UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        #默认保存用户输入的数据
        #通过 form.instance.字段名=值 来进行后端添加
        form.save()

        return redirect("/user/list/")
    else:
        return render(request,'user_edit.html',{'form':form})

#删除用户
def user_delete(request, nid):
    UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
