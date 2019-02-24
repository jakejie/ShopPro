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
from .views import CartView, CartDelView, CartAddView, \
    CartUpdateView, CartCountView, EmptyCartView

urlpatterns = [
    path('user/', CartView.as_view(), name="cart"),
    path('add/', CartAddView.as_view(), name="add_cart"),
    path('del/', CartDelView.as_view(), name="del_cart"),
    path('update/', CartUpdateView.as_view(), name="update_cart"),
    path('count/', CartCountView.as_view(), name="count"),
]
if __name__ == "__main__":
    pass
