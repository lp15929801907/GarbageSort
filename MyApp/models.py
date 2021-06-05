from django.db import models

# Create your models here.


class User(models.Model):  # 用户表
    account = models.CharField(max_length=20, primary_key=True)  # 用户账号
    user_password = models.CharField(max_length=20)  # 用户密码
    user_identity = models.CharField(max_length=20)  # 用户身份


class Common(models.Model):  # 普通用户信息表
    common_id = models.CharField(max_length=20, primary_key=True)  # 普通用户昵称 主键
    common_name = models.CharField(max_length=20)  # 姓名
    common_tel = models.CharField(max_length=20)  # 电话
    common_address = models.CharField(max_length=50)  # 地址
    common_email = models.CharField(max_length=50)  # 邮箱
    common_integral = models.IntegerField(default=0)  # 积分


class Manager(models.Model):  # 管理员信息表
    manager_id = models.CharField(max_length=20, primary_key=True)  # 管理员昵称 主键
    manager_name = models.CharField(max_length=20)  # 姓名
    manager_tel = models.CharField(max_length=20)  # 电话
    manager_email = models.CharField(max_length=50)  # 邮箱


class Type(models.Model):  # 垃圾类型表
    type_id = models.CharField(max_length=20, primary_key=True)  # 垃圾类型编号，主键
    type_name = models.CharField(max_length=20)  # 垃圾类型名称
    type_kind = models.CharField(max_length=1000)  # 垃圾种类


class Dump(models.Model):  # 垃圾回收点信息表
    dump_id = models.CharField(max_length=20, primary_key=True)  # 垃圾回收点编号 主键
    dump_number = models.IntegerField()  # 垃圾桶数量
    dump_place = models.CharField(max_length=20)  # 垃圾回收点位置
    dump_type = models.ForeignKey(Type, on_delete=models.CASCADE)  # 垃圾桶类型


class Throw(models.Model):  # 垃圾投放记录表
    common_id = models.CharField(max_length=20)  # 投放人昵称
    common_tel = models.CharField(max_length=20)  # 投放人联系方式
    dump_id = models.CharField(max_length=20)  # 垃圾回收点编号
    dump_place = models.CharField(max_length=20)  # 垃圾回收点位置
    dump_type = models.ForeignKey(Type, on_delete=models.CASCADE)  # 垃圾桶类型
    throw_time = models.CharField(max_length=20)  # 投放时间

