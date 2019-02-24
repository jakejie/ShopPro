# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:BlogPro
FileName = PyCharm
Version:1.0
CreateDay:2018/4/2 17:14
"""
from product.models import ParentCategory, Category, TagPro, Product, Price, TagAndProduct
from cart.models import CartProduct


def varible(request):
    parent = ParentCategory.objects.all()
    if request.user.is_authenticated:
        cart_list = CartProduct.objects.filter(user_id=request.user.id).all()
    else:
        cart_list = []
    return {
        "parent": parent,
        "cart_list": cart_list,
    }


if __name__ == "__main__":
    pass
