from django.db import models


# Create your models here.
# 管理员
class Admin(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    # 输出显示管理员姓名
    def __str__(self):
        return self.name


class Department(models.Model):
    """部门表"""
    # id = models.BigAutoField(verbose_name='IID', primary = True)
    title = models.CharField(verbose_name='部门名称', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="员工密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    # ax_digits=10  最大长度为10  decimal_places=2  小数点后精确两位   default=2  初始化为0
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    creat_time = models.DateField(verbose_name="入职时间")

    # 添加部门约束ID
    # 使用ForeignKey时 Django自动生成depart_id
    # 如果部门表删除
    # 相关联人员级联删除 on_delete=models.CASCADE
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # 置空
    depart = models.ForeignKey(verbose_name="部门名称", to="Department", to_field="id", null=True, blank=True,
                               on_delete=models.SET_NULL)
    # 创建数据库时应用depart_id

    # 在Django中做的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


# 创建用户
# UserInfo.objects.create(name="nxiaodi", password="123456", age=10, account=100, creat_time="2023.10")

# 添加数据
# Department.objects.create(title="销售部")
# Department.objects.create(title="研发部")


# ##################手机号管理 ##########################
class PrettyNum(models.Model):
    """靓号表"""
    phoneNum = models.CharField(verbose_name="手机号", max_length=11)
    # 想要允许为空 null =True ,blank=True
    price = models.IntegerField(verbose_name="价格")

    level_choices = {
        (1, "一级"),
        (2, "二级"),
        (3, "三级"),
        (4, "四级"),
    }
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)

    status_choices = {
        (1, "已占有"),
        (2, "未使用"),
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """任务"""
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=3)
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """订单"""
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choice = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice, default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    """老板"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.CharField(verbose_name="头像", max_length=128)


class City(models.Model):
    """城市"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    count = models.IntegerField(verbose_name="人口", default=0)
    # 本质上还为CharField，数据库中存储文件路径
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to="city/")

