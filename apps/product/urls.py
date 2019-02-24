# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:ShopPro
FileName = PyCharm
Version:1.0
CreateDay:2018/7/9 14:28
"""
from django.urls import path
from .views import IndexView, ParentCategoryView, CategoryView, TagView, DetailView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("parent/category/<name>/", ParentCategoryView.as_view(), name="parent"),
    path("category/<name>/", CategoryView.as_view(), name="category"),
    path("tag/<name>/", TagView.as_view(), name="tag"),
    path("detail/<product_id>", DetailView.as_view(), name="detail"),
]
if __name__ == "__main__":
    pass
