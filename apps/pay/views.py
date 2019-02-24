import os
import time
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from alipay import AliPay
from ShopPro import settings
from order.models import OrderList

subject = "尚书城图书商城"


# 支付
class PayView(View):
    def get(self, request):
        pass

    def post(self, request):
        order_id = request.POST.get("order_id")
        if order_id:
            order = OrderList.objects.filter(order=order_id).first()
            total_amount = order.totalPrice
            # 创建用于进行支付宝支付的工具对象
            alipay = AliPay(
                appid=settings.ALIPAY_APPID,
                app_notify_url=None,  # 默认回调url, 正常应在这里加上,异步调用返回接口
                app_private_key_path=os.path.join(settings.BASE_DIR, "apps/pay/app_private_2048.txt"),
                alipay_public_key_path=os.path.join(settings.BASE_DIR, "apps/pay/alipay_public_2048.txt"),
                # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                sign_type="RSA2",  # RSA 或者 RSA2
                debug=settings.DEBUG  # 默认False  配合沙箱模式使用
            )
            # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order_id,
                total_amount=str(total_amount),  # 将Decimal类型转换为字符串交给支付宝
                subject=subject,
                # return_url="{}/order/all/".format(settings.HOST),  # 支付成功之后跳转的地址
                return_url="{}/order/detail/order={}/".format(settings.HOST, order.order),  # 支付成功之后跳转的地址
                notify_url=None  # 可选, 不填则使用默认notify url
            )
            # 让用户进行支付的支付宝页面网址
            url = settings.ALIPAY_URL + "?" + order_string
            return JsonResponse({"code": 3, "msg": "请求支付成功", "url": url})
        else:
            return JsonResponse({"code": 0, "msg": "请求支付异常", })


# 检查支付状态
class CheckPayStatusView(View):
    def get(self, request):
        order_id = request.GET.get("order_id", "")
        if order_id:
            # 创建用于进行支付宝支付的工具对象
            alipay = AliPay(
                appid=settings.ALIPAY_APPID,
                app_notify_url=None,  # 默认回调url
                app_private_key_path=os.path.join(settings.BASE_DIR, "apps/pay/app_private_2048.txt"),
                alipay_public_key_path=os.path.join(settings.BASE_DIR, "apps/pay/alipay_public_2048.txt"),
                # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                sign_type="RSA2",  # RSA2,官方推荐，配置公钥的时候能看到
                debug=True  # 默认False  配合沙箱模式使用
            )
            num = 0
            while True:
                # 调用alipay工具查询支付结果
                response = alipay.api_alipay_trade_query(order_id)  # response是一个字典
                # 判断支付结果
                code = response.get("code")  # 支付宝接口调用成功或者错误的标志
                trade_status = response.get("trade_status")  # 用户支付的情况

                if code == "10000" and trade_status == "TRADE_SUCCESS":
                    # 表示用户支付成功 将订单状态设置为已支付
                    order = OrderList.objects.filter(order=order_id).first()
                    order.pay_status = True
                    order.save()
                    # 返回前端json，通知支付成功
                    return JsonResponse({"code": 0, "msg": "支付成功"})

                elif code == "40004" or (code == "10000" and trade_status == "WAIT_BUYER_PAY"):
                    # 表示支付宝接口调用暂时失败，（支付宝的支付订单还未生成） 后者 等待用户支付
                    # 继续查询
                    print(code)
                    print(trade_status)
                    time.sleep(1)
                    num = num + 1
                    if num > 100:
                        # 返回支付失败的通知
                        return JsonResponse({"code": 1, "msg": "支付失败"})
                    else:
                        continue
                else:
                    # 支付失败
                    # 返回支付失败的通知
                    return JsonResponse({"code": 1, "msg": "支付失败"})
        else:
            return JsonResponse({"code": 1, "msg": "订单不存在"})

    def post(self, request):
        pass
