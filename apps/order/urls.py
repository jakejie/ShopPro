# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:ShopPro
FileName = PyCharm
Version:1.0
CreateDay:2018/7/9 15:09
"""
from django.urls import path
from .views import CommitOrderView, OrderCenterView, OrderDetailView

urlpatterns = [
    path("commit/", CommitOrderView.as_view(), name="commit"),
    path("all/", OrderCenterView.as_view(), name="order_info"),
    path('detail/order=<order_id>/', OrderDetailView.as_view(), name="order_detail")
]
if __name__ == "__main__":
    pass
