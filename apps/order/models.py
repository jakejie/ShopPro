from django.db import models
from datetime import datetime

# 支付方式
PAY_METHOD = {
    1: "货到付款",
    2: "微信支付",
    3: "支付宝",
    4: "银联卡支付",
}


# 订单管理
class OrderList(models.Model):
    user = models.ForeignKey("user.UserProfile", verbose_name="用户", on_delete=models.CASCADE)
    order = models.CharField(verbose_name="订单号", max_length=32)
    totalNum = models.IntegerField(verbose_name="总商品数量")
    totalPrice = models.FloatField(verbose_name="总金额")
    pay_method = models.CharField(verbose_name="支付方式", max_length=20, default="")
    pay_status = models.BooleanField(verbose_name="支付状态", default=False)
    address = models.ForeignKey("user.Address", verbose_name="订单收货地址", default=1, on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="下单时间", default=datetime.now)

    class Meta:
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.user, self.order)

    # 获取该订单的商品
    def get_item(self):
        return OrderItem.objects.filter(orderNum=self.order).all()

    # 获取该订单的物流信息
    def get_logistics(self):
        return Logistics.objects.filter(orderNum=self.order).first()


# 订单商品管理
class OrderItem(models.Model):
    orderNum = models.CharField(verbose_name="订单号", max_length=32)
    product = models.ForeignKey("product.Product", verbose_name="商品", on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name="数量")
    add_time = models.DateTimeField(verbose_name="下单时间", default=datetime.now)

    class Meta:
        verbose_name = "订单详情商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.orderNum, self.product.title)


# 物流管理
class Logistics(models.Model):
    SENTTYPECHOICE = (
        ("快递", "express"),
        ("无需物流", "no"),
        ("线下交易", "under_line"),
        ("其他", "other"),
    )
    # orderNum = models.ForeignKey("OrderList", verbose_name="订单号", on_delete=models.CASCADE)
    orderNum = models.CharField(verbose_name="订单号", max_length=32)
    sentType = models.CharField(verbose_name="发货方式", choices=SENTTYPECHOICE, max_length=16)
    name = models.CharField(verbose_name="物流公司", max_length=200, default="")
    num = models.CharField(verbose_name="快递单号", max_length=32, default="0")
    add_time = models.DateTimeField(verbose_name="下单时间", default=datetime.now)

    class Meta:
        verbose_name = "物流管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.orderNum, self.sentType)
