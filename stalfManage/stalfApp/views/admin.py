from django.shortcuts import render, HttpResponse, redirect
from stalfApp import models
from stalfApp.models import Admin
from django.utils.safestring import mark_safe
from stalfApp.utils.pagination import Pagination

import copy
#from django.http.request import QueryDict
from stalfApp.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm

#管理员列表
def admin_list(request):
    # 检查用户是否已经登录，如果未登录，返回登录界面
    # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有
    info = request.session.get("info")
    if info is None:
        return redirect("/login/")


    data_list = Admin.objects.all()

    context = {
        'data_list' : data_list,
    }

    return render(request, 'admin_list.html', context)

def admin_add(request):

    if(request.method == 'GET'):
        form = AdminModelForm()
        context = {
            'form' : form,
        }
        return render(request, 'admin_add.html', context)
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()

        return redirect('/admin/list/')
    else:
        return render(request, 'admin_add.html', {'form' : form})

def admin_edit(request, nid):

    # 对象 / none
    row_object = Admin.objects.filter(id=nid).first()
    # 如果管理员id不存在（None），返回管理员列表
    if not row_object:
        return redirect('/admin/list/')

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'admin_edit.html', {'form' : form})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')


def admin_delete(request, nid):
    Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    # 对象 / none
    row_object = Admin.objects.filter(id=nid).first()
    # 如果管理员id不存在（None），返回管理员列表
    if not row_object:
        return redirect('/admin/list/')

    title = "重置密码 - {}" .format(row_object.name)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'admin_reset.html', {'form' : form, 'title' : title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'admin_reset.html', {'form' : form, 'title' : title})

