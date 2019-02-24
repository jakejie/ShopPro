from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import Product


# 用户管理
class UserProfile(AbstractUser):
    display_name = models.CharField(max_length=100, verbose_name="展示名称", default="")
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(choices=(("male", "男"), ("female", "女")), default="male", max_length=8)
    mobile = models.CharField(max_length=11, default="", verbose_name="手机号码")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.jpg", max_length=100)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 邮箱验证码管理
class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ("register", "注册"),
        ("forget", "找回密码")
    )
    # user = models.ForeignKey("UserProfile", verbose_name="用户", on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, verbose_name="邮箱", default="")
    code = models.CharField(verbose_name="验证码", max_length=64, default="")
    send_type = models.CharField(choices=SEND_CHOICES, max_length=10, verbose_name="验证码类型", default="")
    sent_time = models.DateTimeField(verbose_name="邮件发送时间", default=datetime.now)

    class Meta:
        verbose_name = "邮箱验证码管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.email, self.code)


# 省份
class Province(models.Model):
    name = models.CharField(verbose_name="省份名", max_length=100, default="")
    uid = models.IntegerField(verbose_name="省份ID", default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "省份管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 城市
class City(models.Model):
    province = models.ForeignKey("Province", on_delete=models.CASCADE, verbose_name="省份")
    name = models.CharField(verbose_name="城市名", max_length=100, default="", )
    uid = models.IntegerField(verbose_name="城市ID", default="", )
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "城市管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.province.name, self.name)


# 地区
class Area(models.Model):
    city = models.ForeignKey("City", on_delete=models.CASCADE, verbose_name="城市")
    name = models.CharField(verbose_name="地区名", max_length=100, default="")
    uid = models.IntegerField(verbose_name="地区ID", default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "地区管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.city.name, self.name)


# 地址
class Address(models.Model):
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name="用户")
    is_default = models.BooleanField(default=False, verbose_name="默认地址")
    # 三级城市联动
    # base_add = models.ForeignKey("Area", on_delete=models.CASCADE, verbose_name="基础地址")
    address = models.CharField(verbose_name="基础地址", max_length=300, default="")
    detail = models.CharField(verbose_name="详细地址", max_length=256, default="")
    zip_code = models.CharField(verbose_name="邮编", max_length=10, default="000000")
    mobile = models.CharField(verbose_name="手机号", max_length=11, default="")
    name = models.CharField(verbose_name="收件人姓名", max_length=64, default="")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return "{} {} {}".format(self.user.username,
        #                          self.base_add.city.province.name + self.base_add.city.name + self.base_add.name,
        #                          self.address)
        return "{} {}".format(self.address, self.detail)

    # 获取当前地址的城市 省份 地区
    def get_address_detail(self):
        return "{} {} （{} 收）  {} 邮编：{}".format(
            self.address, self.detail, self.name, self.mobile,self.zip_code
        )
        # return "{} {} {}".format(
        #     self.base_add.city.province.name,
        #     self.base_add.city.name,
        #     self.base_add.name
        # )


# 关注的商品
class FollowProduct(models.Model):
    user = models.ForeignKey("UserProfile", verbose_name="用户", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", verbose_name="商品", on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "关注的商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.user, self.product)


# 推送消息
class PushMessage(models.Model):
    user = models.ForeignKey("UserProfile", verbose_name="用户", on_delete=models.CASCADE)
    message = models.CharField(verbose_name="消息内容", max_length=512)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "推送消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.user, self.message)

# # 聊天记录 客服
# class ChatMessage(models.Model):
#     add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
#
#     pass
