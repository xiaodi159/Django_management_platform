from django.core.exceptions import ValidationError

from stalfApp import models
from django import forms


from stalfApp.utils.bootstrap import BootstrapForm
from stalfApp.utils.encrypt import md5

#管理员
class AdminModelForm(BootstrapForm):
    name = forms.CharField(min_length=3, label="姓名")
    # 添加render_value = True  参数保留原始密码
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ["name", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 添加校验位，对密码进行确认
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data["confirm_password"])
        if pwd != confirm:
            raise ValidationError("密码不一致")
        # 返回什么，字符段保存什么
        return confirm

class AdminEditModelForm(BootstrapForm):
    class Meta:
        model = models.Admin
        fields = ["name"]

class AdminResetModelForm(BootstrapForm):
    # 添加render_value = True  参数保留原始密码
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = models.Admin
        fields = ["password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)

        # 从数据库中获取当前密码，并判断是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("不能与之前密码相同")

        return md5_pwd

    # 添加校验位，对密码进行确认
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data["confirm_password"])
        if pwd != confirm:
            raise ValidationError("密码不一致")
        # 返回什么，字符段保存什么
        return confirm


# ####################### modelform实例 ######################
#继承BootstrapForm 样式
#可以省略def __init__(self, *args, **kwargs): 定义
class UserModelForm(BootstrapForm):
    #如需检验其他信息，需要重新编写规格
    name=forms.CharField(min_length=3,label="姓名")

    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","creat_time","gender","depart"]
        #定义输入框样式
        # widgets = {
        #     "name":forms.TextInput(attrs={"class":"form-cintrol"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-cintrol"})
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     #循环找到所有插件
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class":"form-control"}


#靓号管理
#创建PhoneNum的modelform结构
class PhoneNumMobelFrom(BootstrapForm):
    #如需检验其他信息，需要重新编写规格
    phoneNum = forms.CharField(min_length=11, label="手机号码")

    class Meta:
        model = models.PrettyNum
        fields = ["phoneNum","price","level","status"]

#任务管理系统



