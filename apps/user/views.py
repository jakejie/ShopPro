from django.shortcuts import render
import json
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
# 基于类的视图 继承类
from django.views.generic.base import View
# 引入需要的数据表
from .models import UserProfile, EmailVerifyRecord, Address
# 完成并集查询
from django.db.models import Q
# 定义使用邮箱进行登陆 重载方法
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# 注册/找回密码 邮箱验证
# from utils.email_sent import sent_register_email
# 异步发送邮件
from .tasks import sent_register_email
# 对数据库找出来的内容进行分页
from django.core.paginator import Paginator
from ShopPro.settings import PAGE_SETTING
# 添加消息
from django.contrib import messages


# 发送邮件测试函数
class EmailTestView(View):
    def get(self, request):
        sent_register_email.delay('794564669@qq.com', 'register')
        return HttpResponse("发送成功！")


# 重构 允许使用邮箱/用户名进行登陆
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户注册
class RegisterView(View):
    def get(self, request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "user/register.html", {})

    def post(self, request):
        username = request.POST.get("user_name", "")
        pwd = request.POST.get("pwd", "")
        email = request.POST.get("email", "")
        if all([username, email, pwd]):
            result = UserProfile.objects.filter(username=username).first()
            if result:
                # 当前用户名已经注册
                return render(request, 'user/register.html',
                              {"msg": "用户名被占用！"})
            user = UserProfile(username=username, email=email, password=make_password(pwd), is_active=False)
            user.save()
            print("收到注册请求 准备发送邮箱验证码")
            # 发送邮件 激活==需要异步
            sent_register_email.delay(email, "register")
            # sent_register_email(email, "register")
            # 完成注册操作
            return render(request, 'user/register_complate.html',
                          {"email": email})
        else:
            return render(request, 'user/register.html',
                          {"msg": "用户名/邮箱/密码均不能为空！"})


# 用户激活
class ActivateView(View):
    def get(self, request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        codes = request.GET.get("code")
        code = EmailVerifyRecord.objects.filter(code=codes).first()
        if code:
            email = code.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            # 激活成功 跳转到登陆页面
            return HttpResponseRedirect(reverse("login"))
        else:
            # 激活失败 跳转到注册页
            return HttpResponseRedirect(reverse("register"))

    def post(self, request):
        return render(request, "product/index.html",
                      {})


# 用户登陆
class LoginView(View):
    def get(self, request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, "user/login.html", {})

    def post(self, request):
        # 验证登陆是否成功
        username = request.POST.get("username", "")
        pwd = request.POST.get("pwd", "")
        # print("用户名：{} 密码：{}".format(username, pwd))
        if all([username, pwd]):
            user = authenticate(username=username, password=pwd)
            if user:
                if UserProfile.objects.get(username=username).is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, "user/login.html",
                                  {"msg": "用户尚未激活！去邮箱激活！"})
        return render(request, "user/login.html",
                      {"msg": "用户名或密码错误！"})


# 退出登陆
class LogoutView(View):
    # 退出登陆 跳转到登陆页面
    def get(self, request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            # 已经登陆 退出登陆
            logout(request)
            return HttpResponseRedirect(reverse('login'))
        return HttpResponseRedirect(reverse("index"))

    # 原则上 该视图不会用到
    def post(self, request):
        return render(request, "product/index.html", {})


# 忘记密码/修改密码  后期完成
class ForgetPwdView(View):
    def get(self, request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "user/find_pwd.html", {})

    def post(self, request):
        # 输入邮箱--给邮箱发送验证码--
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        if all([username, email]):
            # 验证用户名和邮箱是否属于同一个用户
            result = UserProfile.objects.filter(
                username=username,
                email=email
            ).first()
            if result:
                # 发送邮件
                sent_register_email.delay(email, "forget")
                # sent_register_email(email, "forget")
                return render(request, "user/find_complate.html",
                              {"email": email})
        return render(request, 'user/find_pwd.html',
                      {"msg": "您输入的用户名或邮箱不对"})


# 检查用户名／邮箱是否一致
class CheckUserEmailView(View):
    def post(self, request):
        username = request.POST.get("username", "")
        email = request.POST.get("email", "")
        if all([username, email]):
            # 验证用户名和邮箱是否属于同一个用户
            result = UserProfile.objects.filter(
                username=username,
                email=email
            ).first()
            if result:
                data = {
                    "code": 3,
                    "msg": "ok"
                }
            else:
                data = {
                    "code": 0,
                    "msg": "用户名或邮箱不存在"
                }
        else:
            data = {
                "code": 0,
                "msg": "用户名或邮箱不能为空"
            }
        return JsonResponse(data)


# 重置密码
class ResetPwdView(View):
    def get(self, request):
        # 如果已经登陆 跳转到主页
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        code = request.GET.get("code", "")
        if code:
            # 找到该验证码
            all_code = EmailVerifyRecord.objects.filter(code=code).last()
            if all_code:
                email = all_code.email
                return render(request, "user/reset_pwd.html",
                              {"email": email})
        return render(request, "product/index.html")

    # 提交新密码
    def post(self, request):
        pwd = request.POST.get("pwd", "")
        email = request.POST.get("email", "")
        if all([pwd, email]):
            user = UserProfile.objects.filter(email=email).first()
            user.password = make_password(password=pwd)
            user.save()
            data = {
                "code": 3,
                "msg": "密码修改成功"
            }
            # return HttpResponseRedirect(reverse("login"))
        else:
            data = {
                "code": 0,
                "msg": "密码修改失败"
            }
            # return render(request, "product/index.html")
        return JsonResponse(data)


# 个人中心
class InfoView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = UserProfile.objects.filter(username=request.user.username).first()
            return render(request, "user/user_center_info.html",
                          {"user": user, })
        else:
            return render(request, 'user/login.html')

    def post(self, request):
        return render(request, "", {})


# 所有地址
class AddressView(View):
    def get(self, request):
        if request.user.is_authenticated:
            address_list = Address.objects.filter(user_id=request.user.id).all()
            return render(request, "user/user_center_site.html",
                          {"address_list": address_list})
        else:
            return render(request, 'user/login.html')

    # 新增地址
    def post(self, request):
        if request.user.is_authenticated:
            is_default = request.POST.get("is_default", False)
            if is_default:
                is_default = True
            name = request.POST.get("name", "")
            s_province = request.POST.get("s_province", "")
            s_city = request.POST.get("s_city", "")
            s_county = request.POST.get("s_county", "")
            detail = request.POST.get("detail_area", "")
            zip_code = request.POST.get("code", "")
            mobile = request.POST.get("mobile", "")
            base_add = "{} {} {}".format(s_province, s_city, s_county)
            if all([is_default, base_add, detail, zip_code, mobile, name]):
                address_info = Address(
                    user_id=request.user.id,
                    is_default=is_default, address=base_add,
                    detail=detail, zip_code=zip_code,
                    mobile=mobile, name=name,
                )
                address_info.save()
                data = {
                    "code": 3,
                    "msg": "添加成功",
                }
            else:
                data = {
                    "code": 0,
                    "msg": "添加失败",
                }
        else:
            data = {
                "code": 0,
                "msg": "添加失败",
            }
        return JsonResponse(data)


# 我的钱包
class WalletView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 我的优惠券
class CouponView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})
