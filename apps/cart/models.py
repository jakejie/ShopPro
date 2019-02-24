from django.db import models
from datetime import datetime
from user.models import UserProfile
from product.models import Product


# 购物车
class CartProduct(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="产品", on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name="数量", default=0)
    commit_target = models.CharField(verbose_name="结算标识符", default="", max_length=36)
    add_time = models.DateTimeField(verbose_name="加入时间", default=datetime.now)

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.user.username, self.product.title)
