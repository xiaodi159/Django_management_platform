from django.shortcuts import render, HttpResponse, redirect

from django.http import JsonResponse

def chart_list(request):
    """数据统计"""
    return render(request, 'chart_list.html')

def chart_bar(request):
    """从数据库中获取数据，返还到图表中"""
    legend = ['xiaodi', 'wangwu']
    xAxis_list = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
    series_list = [
        {
            "name": 'xiaodi',
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20, 12, 23, 45, 23, 10, 30]
        },
        {
            "name": 'wangwu',
            "type": 'bar',
            "data": [12, 3, 20, 40, 20, 50, 13, 24, 56, 7, 1, 34]
        }
    ]
    # 饼状图数据
    pie_data = [
        {"value": 1048, "name": 'IT部'},
        {"value": 735, "name": '宣传部'},
        {"value": 580, "name": '管理部'},
        {"value": 484, "name": '策划部'},
        {"value": 300, "name": '运行部'}
    ]

    results = {
        'status': True,
        'data': {
            'legend': legend,
            'xAxis_list': xAxis_list,
            'series_list': series_list,
            'pie_data': pie_data
        }
    }

    return JsonResponse(results)