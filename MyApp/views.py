import datetime
import re
from django.shortcuts import render
# render方法可接收三个参数，一是request参数，二是待渲染的html模板文件,三是保存具体数据的字典参数。它的作用就是将数据填充进模板文件，最后把结果返回给浏览器。
from MyApp.models import *
account = ""
global_cname = ""
global_mname = ""
# 登录
def login(request):
    return render(request, 'login.html')
# 普通用户注册
def common_register(request):
    name = request.POST.get("common_name")  # 获取用户输入的姓名
    id = request.POST.get("common_id")  # 获取用户输入的昵称
    address = request.POST.get("common_address")  # 获取用户输入的地址
    email = request.POST.get("common_email")  # 获取用户输入的邮箱
    telephone = request.POST.get("common_telephone")  # 获取用户输入的手机号
    ret = re.match(r"^1[35678]\d{9}$", telephone)  # 验证手机号
    password = request.POST.get("common_password")  # 获取用户输入的密码
    result1 = User.objects.filter(account=telephone)  # 在用户表中查询该手机号的记录
    result2 = Common.objects.filter(common_id=id)  # 在普通用户信息表中查询该昵称的记录
    context = {}
    if ret:  # 判断该手机号格式是否正确
        if len(result1) == 1:  # 判断该手机号是否存在(即判断是否注册过)，如果后台存在记录，则返回相应的提示语句
            context["info"] = "该手机号已注册！！！"
            context["status"] = 0  # 零表示注册失败
            return render(request, 'login.html', context=context)
        else:  # 该账号是新用户
            if len(result2) == 1:  # 判断该昵称是否有用户已使用
                context["info"] = "该昵称已占用！！！"
                context["status"] = 4
                return render(request, 'login.html', context=context)
            else:
                User.objects.create(account=telephone, user_password=password,
                                    user_identity='用户')  # 用create为user表添加一条记录
                Common.objects.create(common_name=name, common_id=id, common_address=address, common_tel=telephone,
                                      common_email=email)  # 用create为common表添加一条记录
                context["info"] = "注册成功！"
                context["status"] = 1  # 1表示注册成功
                return render(request, 'login.html', context=context)
    else:
        context["info"] = "手机号格式错误！！！"
        context["status"] = 6
        return render(request, 'login.html', context=context)
# 管理员注册
def manager_register(request):
    id = request.POST.get("manager_id")  # 获取管理员输入的昵称
    telephone = request.POST.get("manager_telephone")  # 获取管理员输入的手机号
    ret = re.match(r"^1[35678]\d{9}$", telephone)  # 验证手机号
    result1 = User.objects.filter(account=telephone)  # 在用户表中查询该手机号的记录
    result2 = Manager.objects.filter(manager_id=id)  # 在管理员信息表中查询该昵称的使用记录
    name = request.POST.get("manager_name")  # 获取管理员输入的姓名
    email = request.POST.get("manager_email")  # 获取管理员输入的邮箱
    password = request.POST.get("manager_password")  # 获取管理员输入的密码
    context = {}
    if ret:  # 判断该手机号格式是否正确
        if len(result1) == 1:  # 判断该手机号是否存在(即判断是否注册过)，如果后台存在记录，则返回相应的提示语句
            context["info"] = "该手机号已注册！！！"
            context["status"] = 0  # 零表示注册失败
            return render(request, 'login.html', context=context)
        else:  # 该账号是新用户
            if len(result2) == 1:  # 判断该昵称号是否有管理员已使用
                context["info"] = "该昵称已占用！！！"
                context["status"] = 5
                return render(request, 'login.html', context=context)
            else:
                User.objects.create(account=telephone, user_password=password,
                                    user_identity='管理员')  # 用create为user表添加一条记录
                Manager.objects.create(manager_name=name, manager_id=id, manager_tel=telephone,
                                       manager_email=email)  # 用create为manager表添加一条记录
                context["info"] = "注册成功！"
                context["status"] = 1  # 1表示注册成功
                return render(request, 'login.html', context=context)
    else:
        context["info"] = "手机号格式错误！！！"
        context["status"] = 6
        return render(request, 'login.html', context=context)
# 登入判定
def login_judge(request):
    global account, global_cname, global_mname  # 定义全局变量account,存储该用户的账号,global_cname保存普通用户的姓名,global_mname保存管理员的姓名
    account = request.POST.get("telephone")  # 获取前端输入的手机号
    user_password = request.POST.get("password")  # 获取前端输入的密码
    result = User.objects.filter(account=account)  # 在user表里查询是否存在该账号
    if len(result) == 1:  # 判断后台是否存在该用户，有则进一步判断密码是否正确
        password = result[0].user_password  # 获取后台的密码
        identity = result[0].user_identity  # 获取该账号的身份信息
        if user_password == password:  # 将用户输入的密码和后台密码进行比对，如果密码一致，判断该账号身份
            if identity == '用户':
                result1 = Common.objects.filter(common_tel=account)
                global_cname = result1[0].common_name  # 用全局变量保存一下该用户的姓名
                context = {
                    "name": result1[0].common_name,
                    "id": result1[0].common_id,
                    "address": result1[0].common_address,
                    "telephone": result1[0].common_tel,
                    "email": result1[0].common_email,
                    "integral": result1[0].common_integral,
                }
                return render(request, 'common/common_information.html', context)  # 跳转到用户主界面
            else:
                result2 = Manager.objects.filter(manager_tel=account)  # account为全局变量
                global_mname = result2[0].manager_name  # 用全局变量保存一下该管理员的姓名
                context = {
                    "name": result2[0].manager_name,
                    "id": result2[0].manager_id,
                    "telephone": result2[0].manager_tel,
                    "email": result2[0].manager_email,
                }
                return render(request, 'manager/manager_information.html', context)  # 跳转到管理员主界面
        else:  # 如果密码不一致，则返回相应提示语句
            context = {
                "info": "密码错误！！！",
                "status": 2
            }
            return render(request, 'login.html', context=context)  # 密码错误返回到登入界面
    else:  # 如果不存在该用户则返回相应的提示语句
        context = {
            "info": "该账号不存在！！！",
            "status": 3
        }
        return render(request, 'login.html', context=context)  # 账号不存在则返回到登入界面

# 普通用户个人信息
def common_information(request):
    if request.method == "GET":  # 此部分是当每次点击侧边导航栏的“查看个人信息”选项时，都重新显示该用户的个人资料
        result = Common.objects.filter(common_tel=account)  # account为全局变量
        context = {
            "name": result[0].common_name,
            "id": result[0].common_id,
            "address": result[0].common_address,
            "telephone": result[0].common_tel,
            "email": result[0].common_email,
            "integral": result[0].common_integral,
        }
        return render(request, 'common/common_information.html', context)  # 将该用户的个人信息再次传到前端页面
    else:  # 在common_information.html页面的第44行中通过post方式的“保存”按钮跳转到此处，即完成更新数据操作（保存）
        id = request.POST.get("id")  # 获取昵称
        address = request.POST.get("address")  # 获取地址
        email = request.POST.get("email")  # 获取邮箱
        Common.objects.filter(common_tel=account).update(common_id=id, common_address=address, common_email=email)  # 更新数据
        result = Common.objects.filter(common_tel=account)  # account为全局变量，此处再次传值到前端
        context = {
            "name": result[0].common_name,
            "id": result[0].common_id,
            "address": result[0].common_address,
            "telephone": result[0].common_tel,
            "email": result[0].common_email,
            "integral": result[0].common_integral,
        }
        return render(request, 'common/common_information.html', context)  # 将该用户的个人信息再次传到前端页面
# 查看垃圾类别
def garbage_type(request):
    types = Type.objects.all()
    return render(request, 'common/garbage_type.html', context={"types": types, "name": global_cname})
# 查找垃圾回收点
def search_dump(request):
    if request.method == "GET":  # 此部分是当用户每次点击侧边导航栏的“查找垃圾回收点”选项时，都要显示出所有垃圾回收点信息
        dumps = Dump.objects.all()
        types = Type.objects.all()
        return render(request, 'common/search_dump.html', context={"dumps": dumps, "types": types, "name": global_cname})  # 向前端传递所有查找到的垃圾回收点信息的集合
    else:  # common/search_dump.html页面中通过post方式的“查询”按钮跳转到此处，即完成查询操作
        dump_place = request.POST.get("dump_place")
        type_id = request.POST.get("type_id")
        types = Type.objects.all()
        if dump_place or type_id:  # 两者中至少有一个不为空
            if dump_place and type_id:  # 两者都不为空
                dump_result = Dump.objects.filter(dump_place=dump_place, dump_type=type_id)
                if dump_result:  # 如果找到的结果集非空，则输出
                    return render(request, 'common/search_dump.html', context={"dumps": dump_result, "types": types, "name": global_cname})
                else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点中该类型的垃圾桶！
                    dump_result = Dump.objects.all()
                    return render(request, 'common/search_dump.html', context={"dumps": dump_result, "types": types, "name": global_cname, "status": 2})
            else:  # 两者中一个不为空
                if dump_place:  # 如果垃圾回收点非空，则按垃圾回收点查找
                    dump_result = Dump.objects.filter(dump_place=dump_place)
                    if dump_result:  # 如果找到的结果集非空，则输出
                        return render(request, 'common/search_dump.html', context={"dumps": dump_result, "types": types, "name": global_cname})
                    else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点！
                        dump_result = Dump.objects.all()
                        return render(request, 'common/search_dump.html', context={"dumps": dump_result, "types": types, "name": global_cname, "status": 0})
                else:  # 如果获取的类型输入框内容不为空，则按类型查找
                    dump_result = Dump.objects.filter(dump_type=type_id)
                    if dump_result:  # 如果找到的结果集非空，则输出
                        return render(request, 'common/search_dump.html', context={"dumps": dump_result, "types": types, "name": global_cname})
                    else:  # 若查询的结果集为0，那么输出未找到该类型的垃圾桶！
                        dump_result = Dump.objects.all()
                        return render(request, 'common/search_dump.html', context={"dumps": dump_result, "types": types, "name": global_cname, "status": 1})
        else:  # 两者都为空
            dump_result = Dump.objects.all()
            return render(request, 'common/search_dump.html', context={"dumps": dump_result, "types": types, "name": global_cname, "status": 3})
# 投放垃圾
def throw_dump(request):
    dump_id = request.GET.get("dump_dump_id")
    result = Dump.objects.filter(dump_id=dump_id).first()
    dumps = Dump.objects.all()
    types = Type.objects.all()
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  # 获取当前投放垃圾的系统时间
    common = Common.objects.filter(common_tel=account).first()
    integral = common.common_integral + 1  # 每投放一次，获得1积分
    Common.objects.filter(common_tel=account).update(common_integral=integral)  # 更新common数据
    Throw.objects.create(common_id=common.common_id, common_tel=account, dump_id=result.dump_id, dump_place=result.dump_place, dump_type=result.dump_type, throw_time=now_time)
    return render(request, 'common/search_dump.html', context={"dumps": dumps, "types": types, "name": global_cname})  # 向前端传递所有查找到的垃圾回收点信息的集合
# 查看个人投放记录
def throw_record(request):
    if request.method == "GET":  # 此部分是当用户每次点击侧边导航栏的“查找个人投放记录”选项时，都要显示出所有投放记录信息
        records = Throw.objects.filter(common_tel=account)  # 把当前用户的投放记录查询出来
        return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname})
    else:  # common/throw_record.html页面中通过post方式的“查询”按钮跳转到此处，即完成查询操作
        dump_place = request.POST.get("dump_place")
        type_id = request.POST.get("type_id")
        if dump_place or type_id:  # 两者中至少有一个不为空
            if dump_place and type_id:  # 两者都不为空
                records = Throw.objects.filter(common_tel=account, dump_place=dump_place, dump_type=type_id)
                if records:  # 如果找到的结果集非空，则输出
                    return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname})
                else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点中该类型的垃圾桶！
                    records = Throw.objects.filter(common_tel=account)
                    return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname, "status": 2})
            else:  # 两者中一个不为空
                if dump_place:  # 如果垃圾回收点非空，则按垃圾回收点查找
                    records = Throw.objects.filter(common_tel=account, dump_place=dump_place)
                    if records:  # 如果找到的结果集非空，则输出
                        return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname})
                    else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点！
                        records = Throw.objects.filter(common_tel=account)
                        return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname, "status": 0})
                else:  # 如果获取的类型输入框内容不为空，则按类型查找
                    records = Throw.objects.filter(common_tel=account, dump_type=type_id)
                    if records:  # 如果找到的结果集非空，则输出
                        return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname})
                    else:  # 若查询的结果集为0，那么输出未找到该类型的垃圾桶！
                        records = Throw.objects.filter(common_tel=account)
                        return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname, "status": 1})
        else:  # 两者都为空
            records = Throw.objects.filter(common_tel=account)
            return render(request, 'common/throw_record.html', context={"records": records, "name": global_cname, "status": 3})
# 分析单用户投放记录数据
def common_analysis(request):
    record = Throw.objects.filter(common_tel=account)  # 把当前用户所有的投放记录查询出来
    record1 = Throw.objects.filter(common_tel=account, dump_type="A")  # 把当前用户投放可回收垃圾的记录查询出来
    record2 = Throw.objects.filter(common_tel=account, dump_type="B")  # 把当前用户投放厨余垃圾的记录查询出来
    record3 = Throw.objects.filter(common_tel=account, dump_type="C")  # 把当前用户投放有害垃圾的记录查询出来
    record4 = Throw.objects.filter(common_tel=account, dump_type="D")  # 把当前用户投放其他垃圾的记录查询出来
    count = len(record)
    count1 = len(record1)
    count2 = len(record2)
    count3 = len(record3)
    count4 = len(record4)
    return render(request, 'common/common_analysis.html', context={"count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4,  "name": global_cname})
# 修改密码
def change_password(request):
    result = User.objects.filter(account=account).first()
    password = result.user_password
    if request.method == "GET":  # 此部分是当每次点击侧边导航栏的“修改密码”选项时，显示该界面
        return render(request, 'common/change_password.html', context={"password": password, "name": global_cname})
    else:  # 此部分是在change_password.html页面中点击保存按钮时完成修改密码的操作
        oldPassword = request.POST.get("oldPassword")
        newPassword = request.POST.get("newPassword")
        reNewPassword = request.POST.get("reNewPassword")  # 以下是先判断输入的旧密码是否正确，并且两次输入的密码是否一致且都不为空
        if password == oldPassword and newPassword == reNewPassword and newPassword and reNewPassword:
            User.objects.filter(account=account).update(user_password=newPassword)  # 更新该用户的密码
            password = newPassword
        return render(request, 'common/change_password.html', context={"password": password, "name": global_cname})

# 管理员个人信息
def manager_information(request):
    if request.method == "GET":  # 此部分是当每次点击侧边导航栏的“查看个人信息”选项时，都重新显示该管理员的个人资料
        result = Manager.objects.filter(manager_tel=account)  # account为全局变量
        context = {
            "name": result[0].manager_name,
            "id": result[0].manager_id,
            "telephone": result[0].manager_tel,
            "email": result[0].manager_email,
        }
        return render(request, 'manager/manager_information.html', context)  # 将该管理员的个人信息再次传到前端页面
    else:  # 在manager_information.html页面的第44行中通过post方式的“保存”按钮跳转到此处，即完成更新数据操作（保存）
        id = request.POST.get("id")  # 获取昵称
        email = request.POST.get("email")  # 获取邮箱
        Manager.objects.filter(manager_tel=account).update(manager_id=id, manager_email=email)  # 更新数据
        result = Manager.objects.filter(manager_tel=account)  # account为全局变量   此处再次传值到前端
        context = {
            "name": result[0].manager_name,
            "id": result[0].manager_id,
            "telephone": result[0].manager_tel,
            "email": result[0].manager_email,
        }
        return render(request, 'manager/manager_information.html', context)  # 将该管理员的个人信息再次传到前端页面
# 管理注册用户
def manage_common(request):
    if request.method == "GET":
        commons = Common.objects.all()  # 把所有用户查询出来
        return render(request, 'manager/manage_common.html', context={"commons": commons, "name": global_mname})
    else:  # manager/manage_common.html页面中通过post方式的“查询”按钮跳转到此处，即完成查询操作
        common_address = request.POST.get("common_address")
        if common_address:  # 如果用户地址非空，则按用户地址查找
            commons = Common.objects.filter(common_address=common_address)
            if commons:  # 如果找到的结果集非空，则输出
                return render(request, 'manager/manage_common.html', context={"commons": commons, "name": global_mname})
            else:  # 若查询的结果集为0，那么输出未找到该地区的注册用户！
                commons = Common.objects.all()  # 把所有用户查询出来
                return render(request, 'manager/manage_common.html', context={"commons": commons, "name": global_mname, "status": 0})
        else:  # 如果用户地址为空，则输出提示信息！
            commons = Common.objects.all()  # 把所有用户查询出来
            return render(request, 'manager/manage_common.html', context={"commons": commons, "name": global_mname, "status": 1})
# 删除注册用户
def delete_common(request):
    if request.method == "GET":
        common_tel = request.GET.get("common_tel")
        Common.objects.filter(common_tel=common_tel).delete()  # 当点击删除按钮后，在common表删除该用户
        User.objects.filter(account=common_tel).delete()  # 当点击删除按钮后，在user表删除该用户
        commons = Common.objects.all()  # 把所有用户查询出来
        return render(request, 'manager/manage_common.html', context={"commons": commons, "status": 2, "name": global_mname})
# 管理垃圾回收点
def manage_dump(request):
    if request.method == "GET":  # 此部分是当用户每次点击侧边导航栏的“管理垃圾回收点”选项时，都要显示出所有垃圾回收点资料
        dumps = Dump.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_dump.html', context={"dumps": dumps, "types": types, "name": global_mname})  # 向前端传递所有查找到的垃圾回收点信息的集合
    else:  # 在manager/manage_bok.html页面中通过post方式的“查询”按钮跳转到此处，即完成查询操作
        dump_place = request.POST.get("dump_place")
        type_id = request.POST.get("type_id")
        types = Type.objects.all()
        if dump_place or type_id:  # 两者中至少有一个不为空
            if dump_place and type_id:  # 两者都不为空
                dump_result = Dump.objects.filter(dump_place=dump_place, dump_type=type_id)
                if dump_result:  # 如果找到的结果集非空，则输出
                    return render(request, 'manager/manage_dump.html', context={"dumps": dump_result, "types": types, "name": global_mname})
                else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点！
                    dump_result = Dump.objects.all()
                    return render(request, 'manager/manage_dump.html', context={"dumps": dump_result, "types": types, "name": global_mname, "status": 2})
            else:  # 两者中一个不为空
                if dump_place:  # 如果垃圾回收点非空，则按垃圾回收点查找
                    dump_result = Dump.objects.filter(dump_place=dump_place)
                    if dump_result:  # 如果找到的结果集非空，则输出
                        return render(request, 'manager/manage_dump.html', context={"dumps": dump_result, "types": types, "name": global_mname})
                    else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点！
                        dump_result = Dump.objects.all()
                        return render(request, 'manager/manage_dump.html', context={"dumps": dump_result, "types": types, "name": global_mname, "status": 0})
                else:  # 如果获取的类型输入框内容不为空，则按类型查找
                    dump_result = Dump.objects.filter(dump_type=type_id)
                    if dump_result:  # 如果找到的结果集非空，则输出
                        return render(request, 'manager/manage_dump.html', context={"dumps": dump_result, "types": types, "name": global_mname})
                    else:  # 若查询的结果集为0，那么输出未找到类型的垃圾桶！
                        dump_result = Dump.objects.all()
                        return render(request, 'manager/manage_dump.html', context={"dumps": dump_result, "types": types, "name": global_mname, "status": 1})
        else:  # 两者都为空
            dump_result = Dump.objects.all()
            return render(request, 'manager/manage_dump.html', context={"dumps": dump_result, "types": types, "name": global_mname, "status": 3})
# 增加垃圾桶的数量
def add_dump(request):
    if request.method == "GET":
        dump_id = request.GET.get("dump_dump_id1")
        result = Dump.objects.filter(dump_id=dump_id).first()
        number = result.dump_number+1  # 让该垃圾桶数量++
        Dump.objects.filter(dump_id=dump_id).update(dump_number=number)
        dumps = Dump.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_dump.html', context={"dumps": dumps, "types": types, "name": global_mname})  # 向前端传递所有查找到的垃圾桶信息的集合
# 减少垃圾桶的数量
def reduce_dump(request):
    if request.method == "GET":
        dump_id = request.GET.get("dump_dump_id2")
        result = Dump.objects.filter(dump_id=dump_id).first()
        number = result.dump_number-1  # 让该垃圾回收点数量--
        Dump.objects.filter(dump_id=dump_id).update(dump_number=number)
        dumps = Dump.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_dump.html', context={"dumps": dumps, "types": types, "name": global_mname})  # 向前端传递所有查找到的垃圾回收点信息的集合
# 删除该垃圾回收点
def delete_dump(request):
    if request.method == "GET":
        dump_id = request.GET.get("dump_id")
        Dump.objects.filter(dump_id=dump_id).delete()  # 在dump表里删除该条记录
        dumps = Dump.objects.all()
        types = Type.objects.all()
        return render(request, 'manager/manage_dump.html', context={"dumps": dumps, "types": types, "status": 4, "name": global_mname})  # 向前端传递所有查找到的垃圾回收点信息的集合
# 修改垃圾回收点详情
def alter_dump(request):
    types = Type.objects.all()
    if request.method == "GET":  # 此部分是当用户在manage_dump.html页面中点击修改垃圾回收点时执行，目的是显示当前垃圾回收点的信息
        dump_id = request.GET.get("dump_dump_id3")
        result = Dump.objects.filter(dump_id=dump_id).first()
        context = {
            "dump_id": result.dump_id,
            "dump_number": result.dump_number,
            "dump_place": result.dump_place,
            "type_name": result.dump_type.type_name,
            "name": global_mname,
            "types": types
        }
        return render(request, 'manager/alter_dump.html', context)  # 向前端传递该垃圾回收点的所有信息
    else:  # 此部分是当用户在alter_dump.html页面中点击确认按钮后重新更新用户修改后的信息
        dump_id = request.POST.get("dump_id")
        dump_number = request.POST.get("dump_number")
        dump_place = request.POST.get("dump_place")
        type_name = request.POST.get("type_name")
        if dump_number.isdigit():  # 判断输入的垃圾桶数量是否为数字
            type = Type.objects.filter(type_name=type_name).first()  # 垃圾桶类型是外键
            Dump.objects.filter(dump_id=dump_id).update(dump_number=dump_number, dump_place=dump_place, dump_type=type)  # 在dump表里更新刚才修改的垃圾回收点信息
            context = {  # 把修改后的内容显示出来
                "dump_id": dump_id,
                "dump_number": dump_number,
                "dump_place": dump_place,
                "type_name": type_name,
                "name": global_mname,
                "types": types,
                "status": 1
            }
            return render(request, 'manager/alter_dump.html', context)  # 重新向前端传递该垃圾回收点的所有信息
        else:
            result = Dump.objects.filter(dump_id=dump_id).first()
            context = {
                "dump_id": result.dump_id,
                "dump_number": result.dump_number,
                "dump_place": result.dump_place,
                "type_name": result.dump_type.type_name,
                "name": global_mname,
                "types": types,
                "status": 2
            }
            return render(request, 'manager/alter_dump.html', context)  # 向前端传递该垃圾回收点的所有信息
# 添加新垃圾回收点
def add_new_dump(request):
    types = Type.objects.all()
    if request.method == "GET":  # 此部分是当每次点击侧边导航栏的“添加垃圾回收点”选项时，显示该界面
        return render(request, 'manager/add_new_dump.html', context={"name": global_mname, "types": types})
    else:  # 此部分是在add_new_dump.html页面中点击确认按钮后完成的添加垃圾回收点操作
        dump_id = request.POST.get("dump_id")  # 获取用户在前端输入框中的数据
        dump_number = request.POST.get("dump_number")
        dump_place = request.POST.get("dump_place")
        type_name = request.POST.get("type_name")
        result = Dump.objects.filter(dump_id=dump_id)  # 在垃圾回收表中查询该编号的记录
        if len(result) == 1:  # 判断该编号是否存在，如果后台存在记录，则返回相应的提示语句
            return render(request, 'manager/add_new_dump.html', context={"name": global_mname, "types": types, "status": 0})
        else:  # 该编号未使用
            if dump_number.isdigit():  # 判断输入的垃圾桶数量是否为数字
                type = Type.objects.filter(type_name=type_name).first()  # 垃圾桶类型是外键
                Dump.objects.create(dump_id=dump_id, dump_number=dump_number, dump_place=dump_place, dump_type=type)  # 在dump表里添加新记录
                return render(request, 'manager/add_new_dump.html', context={"name": global_mname, "types": types, "status": 1})
            else:
                return render(request, 'manager/add_new_dump.html', context={"name": global_mname, "types": types, "status": 2})
# 查看所有投放记录
def search_record(request):
    if request.method == "GET":
        commons = Common.objects.all()  # 把所有用户查询出来
        records = Throw.objects.all()  # 把所有的投放记录查询出来
        return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname})
    else:  # manager/search_record.html页面中通过post方式的“查询”按钮跳转到此处，即完成查询操作
        commons = Common.objects.all()  # 把所有用户查询出来
        common_tel = request.POST.get("common_tel")
        dump_place = request.POST.get("dump_place")
        if common_tel or dump_place:  # 两者中至少有一个不为空
            if common_tel and dump_place:  # 两者都不为空
                records = Throw.objects.filter(common_tel=common_tel, dump_place=dump_place)
                if records:  # 如果找到的结果集非空，则输出
                    return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname})
                else:  # 若查询的结果集为0，那么输出未找到该用户在该垃圾回收点的投放记录！
                    records = Throw.objects.all()
                    return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname, "status": 2})
            else:  # 两者中一个不为空
                if common_tel:  # 如果用户非空，则按用户查找
                    records = Throw.objects.filter(common_tel=common_tel)
                    if records:  # 如果找到的结果集非空，则输出
                        return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname})
                    else:  # 若查询的结果集为0，那么输出未找到该用户的投放记录！
                        records = Throw.objects.all()
                        return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname, "status": 0})
                else:  # 如果获取的垃圾回收点输入框内容不为空，则按垃圾回收点查找
                    records = Throw.objects.filter(dump_place=dump_place)
                    if records:  # 如果找到的结果集非空，则输出
                        return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname})
                    else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点的投放记录！
                        records = Throw.objects.all()
                        return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname, "status": 1})
        else:  # 两者都为空
            records = Throw.objects.all()
            return render(request, 'manager/search_record.html', context={"commons": commons, "records": records, "name": global_mname, "status": 3})
# 分析所有的投放记录
def manage_analysis(request):
    if request.method == "GET":
        commons = Common.objects.all()  # 把所有用户查询出来
        records = Throw.objects.all()  # 把所有用户的投放记录查询出来
        record1 = Throw.objects.filter(dump_type="A")  # 把所有用户投放可回收垃圾的记录查询出来
        record2 = Throw.objects.filter(dump_type="B")  # 把所有用户投放厨余垃圾的记录查询出来
        record3 = Throw.objects.filter(dump_type="C")  # 把所有用户投放有害垃圾的记录查询出来
        record4 = Throw.objects.filter(dump_type="D")  # 把所有用户投放其他垃圾的记录查询出来
        count = len(records)
        count1 = len(record1)
        count2 = len(record2)
        count3 = len(record3)
        count4 = len(record4)
        return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname})
    else:  # manager/search_record.html页面中通过post方式的“查询”按钮跳转到此处，即完成查询操作
        commons = Common.objects.all()  # 把所有用户查询出来
        common_tel = request.POST.get("common_tel")
        dump_place = request.POST.get("dump_place")
        if common_tel or dump_place:  # 两者中至少有一个不为空
            if common_tel and dump_place:  # 两者都不为空
                records = Throw.objects.filter(common_tel=common_tel, dump_place=dump_place)
                if records:  # 如果找到的结果集非空，则输出
                    record1 = Throw.objects.filter(common_tel=common_tel, dump_place=dump_place, dump_type="A")
                    record2 = Throw.objects.filter(common_tel=common_tel, dump_place=dump_place, dump_type="B")
                    record3 = Throw.objects.filter(common_tel=common_tel, dump_place=dump_place, dump_type="C")
                    record4 = Throw.objects.filter(common_tel=common_tel, dump_place=dump_place, dump_type="D")
                    count = len(records)
                    count1 = len(record1)
                    count2 = len(record2)
                    count3 = len(record3)
                    count4 = len(record4)
                    return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname})
                else:  # 若查询的结果集为0，那么输出未找到该用户在该垃圾回收点的投放记录！
                    records = Throw.objects.all()  # 把所有用户的投放记录查询出来
                    record1 = Throw.objects.filter(dump_type="A")  # 把所有用户投放厨余垃圾的记录查询出来
                    record2 = Throw.objects.filter(dump_type="B")  # 把所有用户投放可回收垃圾的记录查询出来
                    record3 = Throw.objects.filter(dump_type="C")  # 把所有用户投放有害垃圾的记录查询出来
                    record4 = Throw.objects.filter(dump_type="D")  # 把所有用户投放其他垃圾的记录查询出来
                    count = len(records)
                    count1 = len(record1)
                    count2 = len(record2)
                    count3 = len(record3)
                    count4 = len(record4)
                    return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname, "status": 2})
            else:  # 两者中一个不为空
                if common_tel:  # 如果用户非空，则按用户查找
                    records = Throw.objects.filter(common_tel=common_tel)
                    if records:  # 如果找到的结果集非空，则输出
                        record1 = Throw.objects.filter(common_tel=common_tel, dump_type="A")
                        record2 = Throw.objects.filter(common_tel=common_tel, dump_type="B")
                        record3 = Throw.objects.filter(common_tel=common_tel, dump_type="C")
                        record4 = Throw.objects.filter(common_tel=common_tel, dump_type="D")
                        count = len(records)
                        count1 = len(record1)
                        count2 = len(record2)
                        count3 = len(record3)
                        count4 = len(record4)
                        return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname})
                    else:  # 若查询的结果集为0，那么输出未找到该用户的投放记录！
                        records = Throw.objects.all()  # 把所有用户的投放记录查询出来
                        record1 = Throw.objects.filter(dump_type="A")  # 把所有用户投放厨余垃圾的记录查询出来
                        record2 = Throw.objects.filter(dump_type="B")  # 把所有用户投放可回收垃圾的记录查询出来
                        record3 = Throw.objects.filter(dump_type="C")  # 把所有用户投放有害垃圾的记录查询出来
                        record4 = Throw.objects.filter(dump_type="D")  # 把所有用户投放其他垃圾的记录查询出来
                        count = len(records)
                        count1 = len(record1)
                        count2 = len(record2)
                        count3 = len(record3)
                        count4 = len(record4)
                        return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname, "status": 0})
                else:  # 如果获取的垃圾回收点输入框内容不为空，则按垃圾回收点查找
                    records = Throw.objects.filter(dump_place=dump_place)
                    if records:  # 如果找到的结果集非空，则输出
                        record1 = Throw.objects.filter(dump_place=dump_place, dump_type="A")
                        record2 = Throw.objects.filter(dump_place=dump_place, dump_type="B")
                        record3 = Throw.objects.filter(dump_place=dump_place, dump_type="C")
                        record4 = Throw.objects.filter(dump_place=dump_place, dump_type="D")
                        count = len(records)
                        count1 = len(record1)
                        count2 = len(record2)
                        count3 = len(record3)
                        count4 = len(record4)
                        return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname})
                    else:  # 若查询的结果集为0，那么输出未找到该垃圾回收点的投放记录！
                        records = Throw.objects.all()  # 把所有用户的投放记录查询出来
                        record1 = Throw.objects.filter(dump_type="A")  # 把所有用户投放厨余垃圾的记录查询出来
                        record2 = Throw.objects.filter(dump_type="B")  # 把所有用户投放可回收垃圾的记录查询出来
                        record3 = Throw.objects.filter(dump_type="C")  # 把所有用户投放有害垃圾的记录查询出来
                        record4 = Throw.objects.filter(dump_type="D")  # 把所有用户投放其他垃圾的记录查询出来
                        count = len(records)
                        count1 = len(record1)
                        count2 = len(record2)
                        count3 = len(record3)
                        count4 = len(record4)
                        return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname, "status": 1})
        else:  # 两者都为空
            records = Throw.objects.all()  # 把所有用户的投放记录查询出来
            record1 = Throw.objects.filter(dump_type="A")  # 把所有用户投放厨余垃圾的记录查询出来
            record2 = Throw.objects.filter(dump_type="B")  # 把所有用户投放可回收垃圾的记录查询出来
            record3 = Throw.objects.filter(dump_type="C")  # 把所有用户投放有害垃圾的记录查询出来
            record4 = Throw.objects.filter(dump_type="D")  # 把所有用户投放其他垃圾的记录查询出来
            count = len(records)
            count1 = len(record1)
            count2 = len(record2)
            count3 = len(record3)
            count4 = len(record4)
            return render(request, 'manager/manage_analysis.html', context={"commons": commons, "count": count, "count1": count1, "count2": count2, "count3": count3, "count4": count4, "name": global_mname, "status": 3})
# 删除投放记录
def delete_record(request):
    if request.method == "GET":
        throw_id = request.GET.get("id")
        Throw.objects.filter(id=throw_id).delete()  # 当点击删除按钮后，删除该投放记录
        records = Throw.objects.all()  # 把当前投放记录查询出来
        return render(request, 'manager/search_record.html', context={"records": records, "status": 4, "name": global_mname})
# 修改管理员的密码
def change_manager_password(request):
    result = User.objects.filter(account=account).first()
    password = result.user_password
    if request.method == "GET":  # 此部分是当每次点击侧边导航栏的“修改密码”选项时，显示该界面
        return render(request, 'manager/change_manager_password.html', context={"password": password, "name": global_mname})
    else:  # 此部分是在change_manager_password.html页面中点击保存按钮时完成修改密码的操作
        oldPassword = request.POST.get("oldPassword")
        newPassword = request.POST.get("newPassword")
        reNewPassword = request.POST.get("reNewPassword")  # 以下是先判断输入的旧密码是否正确，并且两次输入的密码是否一致且都不为空
        if password == oldPassword and newPassword == reNewPassword and newPassword and reNewPassword:
            User.objects.filter(account=account).update(user_password=newPassword)  # 更新该用户的密码
            password = newPassword
        return render(request, 'manager/change_manager_password.html', context={"password": password, "name": global_mname})
