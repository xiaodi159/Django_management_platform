import os

from django.shortcuts import render, HttpResponse, redirect
from django import forms
from django.db import models
# from django.core import settings

from stalfApp import models
from stalfApp.utils.bootstrap import BootstrapForm


class UpForm(forms.Form):
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')

    # print(request.POST)
    # 获取文件
    # print(request.FILES)
    file_object = request.FILES.get("avatar")
    print(file_object.name)

    # 保存文件至项目
    file_path = "stalfApp/static/img/"
    # full_file_path = file_path + file_object.name
    f = open(file_path + file_object.name, 'wb')
    for chunk in file_object.chunks():
        f.write(chunk)
    f.close()

    return HttpResponse("!!!!")


def upload_form(request):
    """文件上传，Form表单验证"""
    title = "Form上传"
    if request.method == 'GET':
        form = UpForm()
        context = {
            "title": title,
            "form": form,
        }
        return render(request, 'upload_form.html', context)
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取文件路径，保存到项目目录中
        image_object = form.cleaned_data.get("img")

        media_path = os.path.join("media", image_object.name)
        f = open(media_path, mode='wb')
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        # 将图片路径，写入到数据库中
        models.Boss.objects.create(
            name=form.cleaned_data.get("name"),
            age=form.cleaned_data.get("age"),
            img=media_path,
        )

        # # file_path = "stalfApp/static/img/{}".format(image_object.name)
        # db_file_path = os.path.join("static", "img", image_object.name)
        # file_path = os.path.join("stalfApp", db_file_path)
        # f = open(file_path, mode='wb')
        # for chunk in image_object.chunks():
        #     f.write(chunk)
        # f.close()
        #
        # # 将图片路径，写入到数据库中
        # models.Boss.objects.create(
        #     name=form.cleaned_data.get("name"),
        #     age=form.cleaned_data.get("age"),
        #     img=db_file_path,
        # )

        return HttpResponse("!!!!")

    return render(request, 'upload_form.html', {'form': form, 'title': title})

class UploadForm(BootstrapForm):
    class Meta:
        model = models.City
        fields = "__all__"


def upload_model_form(request):
    """ModelForm混合文件上传"""
    title = "ModelForm文件上传"
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'upload_model_form.html', {'form': form, 'title': title})

    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 对文件自动保存
        form.save()
        return HttpResponse("上传成功！")
    return render(request, 'upload_model_form.html', {'form': form, 'title': title})
