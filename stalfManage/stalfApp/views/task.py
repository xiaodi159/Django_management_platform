import json
from django import forms

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from stalfApp import models
from stalfApp.utils.bootstrap import BootstrapForm


class TaskModelForm(BootstrapForm):

    class Meta:
        model = models.Task
        fields = '__all__'
        # 定义插件
        widgets = {
            "detail": forms.TextInput,
            # "detail": forms.Textarea,
        }


def task_list(request):
    """
        任务列表
    """
    # 数据库获取所有数据
    queryset = models.Task.objects.all().order_by('-id')
    form = TaskModelForm()
    context = {
        'form': form,
        'queryset': queryset,
    }

    return render(request, 'task_list.html', context)

# 免除csrf cookie认证
@csrf_exempt
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    data_dict = {
        'statud': True,
        'data': [11, 22, 33, 44],
    }
    # return HttpResponse(json.dumps(data_dict))
    return JsonResponse(data_dict)

@csrf_exempt
def task_add(request):
    # print(request.POST)

    # 1、用户发送过来数据通过MoselForm进行校验
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {
            'status': True,
        }
        return HttpResponse(json.dumps(data_dict))
    # 错误信息存储于form.errors中
    data_dict = {
        "status": False,
        "error": form.errors,
    }
    return HttpResponse(json.dumps(data_dict))



