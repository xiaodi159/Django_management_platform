import uuid
import random
from datetime import datetime

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from stalfApp import models
from stalfApp.models import Order
from stalfApp.utils.bootstrap import BootstrapForm


class OrderModelForm(BootstrapForm):
    class Meta:
        model = models.Order
        # fields = '__all__'
        exclude = ['oid', 'admin']


def order_list(request):
    queryset = Order.objects.all().order_by('id')

    form = OrderModelForm()
    context = {
        'queryset': queryset,
        'form': form
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新建订单 ajax"""
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 后台生成oid(订单号）
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))
        # 负责人设置为当前登录的管理员的ID
        form.instance.admin_id = request.session['info']["id"]
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def order_delete(request):
    # 获取id
    uid = request.GET.get('uid')
    # 从数据库查询数据
    exists = models.Order.objects.filter(id=uid).exists()

    # print( uid ,exists)
    if not exists:
        return JsonResponse({'status': False, 'error': "删除失败,数据不存在。"})

    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def order_detail(request):
    """
    # 获取对象
    # 获取id
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'error': "数据不存在"})
    result = {
        'status': True,
        'data':{
            "id": row_object.id,
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
            "admin_id": row_object.admin_id,
        }
    }
    return JsonResponse(result)
    """


    """通过订单id获取订单所有信息"""
    # 获取字典
    # 获取id
    uid = request.GET.get('uid')
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    if not row_dict:
        return JsonResponse({'status': False, 'error': "数据不存在"})
    result = {
        'status': True,
        'data': row_dict,
    }
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    """编辑"""
    uid = request.GET.get('uid')
    row_object = models.Order.objects.filter(id=uid).first()
    # 数据库中数据不存在
    if not row_object:
        return JsonResponse({'status': False, 'tips': "数据不存在"})

    form = OrderModelForm(request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})



