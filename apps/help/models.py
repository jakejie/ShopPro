from django.db import models
from datetime import datetime


# 帮助系统/文章/导航
class HelpArticle(models.Model):
    title = models.CharField(verbose_name="标题", max_length=128)
    detail = models.TextField(verbose_name="文章内容")  # 之后替换为富文本编辑器
    add_time = models.DateTimeField(verbose_name="发布时间", default=datetime.now)

    class Meta:
        verbose_name = "帮助"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.title)
