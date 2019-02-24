from django.db import models
from datetime import datetime


# 一级评论管理
class Comment(models.Model):
    user = models.ForeignKey("user.UserProfile", verbose_name="用户", on_delete=models.CASCADE)
    product = models.ForeignKey("product.Product", verbose_name="产品", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容", max_length=512)
    support = models.IntegerField(verbose_name="点赞", default=0)
    add_time = models.DateTimeField(verbose_name="评论时间", default=datetime.now)

    class Meta:
        verbose_name = "一级评论管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {} {}".format(self.user.username, self.product.title, self.content)


# 二级评论管理
class CommentReply(models.Model):
    user = models.ForeignKey("user.UserProfile", verbose_name="用户", on_delete=models.CASCADE)
    reply = models.ForeignKey("Comment", verbose_name="一级评论", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容", max_length=512)
    add_time = models.DateTimeField(verbose_name="评论时间", default=datetime.now)

    class Meta:
        verbose_name = "二级评论管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{} {}".format(self.user.username, self.content)
