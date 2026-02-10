from django.shortcuts import render, HttpResponse, redirect

from django import forms

from stalfApp.utils.encrypt import md5

from stalfApp.models import Admin

class LoginForm(forms.Form):
    name = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True,  #必填，不能为空
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True,  # 必填，不能为空
    )

    def clean_password(self):
        pwd = self.cleaned_data.pop('password')
        return md5(pwd)

"""
    登录
"""
def login(request):
    if request.method == "GET":
        form = LoginForm()
        # return render(request, 'login.html', {'form': form})
        return render(request, 'enroll.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        #验证成功
        # print(form.cleaned_data)

        # 在数据库中进行校验
        # admin_object = Admin.objects.filter(name=form.cleaned_data['name'], password=form.cleaned_data['password']).first()
        # 获取用户信息
        admin_object = Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            # 主动在form中添加错误
            form.add_error("password", "用户名或密码错误")
            return render(request, 'enroll.html', {'form': form})

        # 用户名和密码正确
        # 网站随机生成字符串， 写到用户的cookie中， 再写入到session中
        request.session["info"] = {
            'id': admin_object.id,
            'name': admin_object.name,
        }
        # return HttpResponse("登陆成功！")
        return redirect('/admin/list/')

    return render(request, 'enroll.html', {'form': form})


def logout(request):
    """注销"""
    request.session.clear()
    return redirect('/login/')


