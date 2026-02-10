"""
    自定义分页组件
"""
from django.utils.safestring import mark_safe

class Pagination(object):
    def __init__(self, request, page_size=10, page_param="page", plus = 5):
        #获取当前页
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        #计算起始页与结束页
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.plus = plus



