"""ShopPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
# from django.views.static import serve
# from django.conf import settings
# from django.conf.urls.static import static
import xadmin
from product.views import IndexView
from user.views import LoginView, RegisterView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index_1"),  # 首页
    path('login/', LoginView.as_view(), name="login_1"),  # 登录页面
    path('register/', RegisterView.as_view(), name="register_1"),  # 注册页面
    path("user/", include("user.urls")),  # 用户相关视图板块
    path("product/", include("product.urls")),  # 产品/商品相关视图板块
    path("cart/", include("cart.urls")),  # 购物车操作相关视图
    path("order/", include("order.urls")),  # 订单相关处理视图　
    path("pay/", include("pay.urls")),  # 支付相关处理
    # 静态文件处理(主要是之前上传的文件等静态资源)========这个bug 应该说这个静态地址 研究了半天
    # path('media/<path:path>/', serve, {"document_root": settings.MEDIA_ROOT}),
    # path('static/<path:path>/', serve, {"document_root": settings.STATIC_ROOT}),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
