# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:ShopPro
FileName = PyCharm
Version:1.0
CreateDay:2018/7/9 13:31
"""
from .views import RegisterView, ActivateView, LoginView, LogoutView, \
    ForgetPwdView, ResetPwdView, InfoView, AddressView, \
    EmailTestView,CheckUserEmailView
from django.urls import path

urlpatterns = [
    path('email/', EmailTestView.as_view(), name='email'),
    path('check/username/',CheckUserEmailView.as_view(),name="check"),
    path('register/', RegisterView.as_view(), name="register"),
    path('activate/', ActivateView.as_view(), name="activate"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('forget/pwd/', ForgetPwdView.as_view(), name="forget"),
    path('reset/password/', ResetPwdView.as_view(), name="reset"),
    path('info/', InfoView.as_view(), name="info"),
    path('address/', AddressView.as_view(), name="address"),
]
if __name__ == "__main__":
    pass
