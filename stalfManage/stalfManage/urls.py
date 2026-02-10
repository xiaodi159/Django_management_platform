"""
URL configuration for stalfManage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stalfApp import views
from stalfApp.views import depart, user, phoneNum, admin, account, task, order, chart, upload, city

from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    # 启用media
    re_path(r'^media/(?P<path>.*)$',serve, {'document_root':settings.MEDIA_ROOT}, name='media'),

    #path('admin/', admin.site.urls),

    path('test/', user.orm),

    #部门管理
    path('depart/list/', depart.depart_list),
    #添加部门列表
    path('depart/add/', depart.depart_add),
    #删除部门信息
    path('depart/delete/', depart.depart_delete),
    #修改信息
    path('depart/<int:nid>/edit/', depart.depart_edit),
    # 通过excel文件上传数据库
    path('depart/multi/', depart.depart_multi),


    #用户管理
    path('user/list/', user.user_list),
    #添加用户
    path('user/add/',user.user_add),
    path('user/modelform/add/', user.modelform_add),
    #编辑用户
    path('user/<int:nid>/edit/',user.user_edit),
    #删除用户
    path('user/<int:nid>/delete/', user.user_delete),


    #靓号管理
    path('phoneNum/list/', phoneNum.phoneNum_list),
    #新建靓号
    path('phoneNum/add/', phoneNum.phoneNum_add),
    #编辑靓号
    path('phoneNum/<int:nid>/edit/', phoneNum.phoneNum_edit),
    #删除靓号
    path('phoneNum/<int:nid>/delete/', phoneNum.phoneNum_delete),

    #管理员管理
    path('admin/list/', admin.admin_list),
    #创建管理员
    path('admin/add/', admin.admin_add),
    #编辑管理员
    path('admin/<int:nid>/edit/', admin.admin_edit),
    #删除管理员
    path('admin/<int:nid>/delete/', admin.admin_delete),
    #重置密码
    path('admin/<int:nid>/reset/', admin.admin_reset),

    #登录
    path('login/', account.login),
    #注销用户
    path('logout/', account.logout),

    #任务管理
    path('task/list/', task.task_list),
    #测试ajax功能
    path('task/ajax/', task.task_ajax),
    path('task/add/', task.task_add),
    # path('task/delete/', task.task_delete),

    # 订单管理
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),

    # 上传文件
    path('upload/list/', upload.upload_list),
    path('upload/form/', upload.upload_form),
    path('upload/model/form/', upload.upload_model_form),

    # 城市列表
    path('city/list/', city.city_list),
    path('city/add/', city.city_add),

]
