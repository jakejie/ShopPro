import time
import uuid
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from cart.models import CartProduct
from .models import OrderList, OrderItem
from user.models import Address
# 分页
from django.core.paginator import Paginator


# 订单号生成规则：用户ID+年月日时分秒+商品数量

# 提交订单
class CommitOrderView(View):
    # 购物车页面 去结算 之后 跳转到此
    def get(self, request):
        if request.user.is_authenticated:
            target = request.GET.get("target", "")
            # print("订单号：{}".format(time.strftime("%Y%m%d%H%M%S")))
            product_list = CartProduct.objects.filter(commit_target=target).all()
            if product_list:
                # 获取默认收货地址
                address_list = Address.objects.filter(user_id=request.user.id).all()
                count = 0  # 商品总数
                total_price = 0  # 总金额
                for product in product_list:
                    count += product.num
                    total_price += product.product.get_price() * product.num
                return render(request, "order/place_order.html",
                              {"product_list": product_list,
                               "count": count,
                               "total_price": total_price,
                               "address_list": address_list,
                               "target": target})
            else:
                return redirect(reverse('order_info'))
        else:
            return render(request, 'user/login.html')

    # POST请求提交订单 跳转到订单中心
    def post(self, request):
        # 提交订单 ①商品内容 ②用户ID 从购物车中删除 生成订单号 生成订单--》跳转到订单中心
        if request.user.is_authenticated:
            # 获取在提交订单页提交过来的数据
            addr_id = request.POST.get("addr_id", "")  # 收货地址
            pay_method = request.POST.get("pay_method", "")  # 支付方式
            target = request.POST.get("target", "")  # 获取需要生成订单的对应商品
            total_price = request.POST.get("total_price", "")  # 订单总金额
            count = request.POST.get("count", "")  # 订单商品总数量
            # 订单号
            order_num = "{}{}{}".format(
                request.user.id, time.strftime("%Y%m%d%H%M%S"), count)
            # 保存订单的商品
            product_list = CartProduct.objects.filter(commit_target=target).all()
            if product_list:
                for product in product_list:
                    item = OrderItem(
                        orderNum=order_num,
                        product_id=product.product.id,
                        num=product.num
                    )
                    item.save()
                # 从购物车中删除
                CartProduct.objects.filter(commit_target=target).delete()
                # print(addr_id, pay_method, target, total_price, count, order_num)
                # 保存订单
                user_order = OrderList(
                    user_id=request.user.id,
                    order=order_num,
                    pay_method=pay_method,
                    totalNum=int(count),
                    totalPrice=float(total_price),
                    address_id=int(addr_id),
                )
                user_order.save()

                data = {
                    "code": 6,
                    "msg": "正常 跳转",
                }
            else:
                data = {
                    "code": 2,
                    "msg": "请求错误 刷新后重试！"
                }
        else:
            data = {
                "code": 2,
                "msg": "请登陆后重试！"
            }
        return JsonResponse(data)


# 订单中心/查看所有订单---》去支付
class OrderCenterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            page = request.GET.get("page", "")
            if not page:
                page = 1
            order_list = OrderList.objects.filter(user_id=request.user.id).all().order_by('-id')
            paginator = Paginator(order_list, 5)  # 分页对象
            contacts = paginator.get_page(page)
            return render(request, "order/user_center_order.html",
                          {"contacts": contacts})
        else:
            return render(request, 'user/login.html')

    def post(self, request):
        return render(request, "", {})


# 订单详情
class OrderDetailView(View):
    def get(self, request, order_id):
        if request.user.is_authenticated:
            result = OrderList.objects.filter(
                order=order_id, user_id=request.user.id
            ).first()
            if result:
                return render(request, "order/order_detail.html",
                              {"order_detail": result})
            # 请求错误
            return ""
        else:
            return render(request, 'user/login.html')

    def post(self, request):
        return render(request, "", {})


# 待支付订单
class WaitPayOrderView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 待收货订单
class WaitTakeOrderView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 待评价订单
class WaitCommentOrderView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 售后服务订单
class ServiceOrderView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 正在支付订单
class PayOrderView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 查看物流
class OrderLogisticsView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})
