from django.shortcuts import render, HttpResponse, redirect

from stalfApp import models
from stalfApp.utils.bootstrap import BootstrapForm

def city_list(request):
    queryset = models.City.objects.all()

    return render(request, 'city_list.html', {'city_list': queryset})


class UploadForm(BootstrapForm):
    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """ModelForm混合文件上传"""
    title = "新建城市(ModelForm)"
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'upload_model_form.html', {'form': form, 'title': title})

    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对文件自动保存
        # 如果上传图片相同，自动在重复图片名称后添加字符串进行区别
        form.save()
        return redirect('/city/list/')
    return render(request, 'upload_model_form.html', {'form': form, 'title': title})