from django.utils.deprecation import MiddlewareMixin

from django.shortcuts import render, HttpResponse, redirect

"""
    通过中间组件实现完善的登录界面
    当管理员成功登录后才可进行系统的管理
"""


class AuthMiddleware(MiddlewareMixin):
    """中间件1"""
    def process_request(self, request):
        # 如果方法中没有返回值（返回None），继续向后走
        # 如果有返回值，则不再向后执行
        # print("M1,进来了")

        # 排除不需要验证就可以访问的登录页面
        if request.path_info == '/login/' or request.path_info == '/admin/add/':
            return

        #获取当前登录用户信息
        info_dict = request.session.get('info')
        # print(info_dict)
        if info_dict:
            return
        # 没有登录，返回登录界面
        return redirect('/login/')

    def process_response(self, request, response):
        # print("M1,走了")
        return response


