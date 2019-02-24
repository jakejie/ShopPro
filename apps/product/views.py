from django.shortcuts import render
# 基于类的视图 继承类
from django.views.generic.base import View
from django.views.generic import ListView
# 数据表Model
from .models import ParentCategory, Category, TagPro, Product, Price, TagAndProduct
# 分页
from django.core.paginator import Paginator


# 首页/主页
class IndexView(View):
    def get(self, request):
        return render(request, "product/index.html", {

        })

    def post(self, request):
        return render(request, "", {

        })


# 分类页/一级分类
class ParentCategoryView(View):
    def get(self, request, name):
        page = request.GET.get("page", "")
        # 排序方式
        sort = request.GET.get("sort", "")
        if not sort:
            sort = "default"
        if not page:
            page = 1
        content = TagAndProduct.objects.filter(tag__father__father__slug=name).all().order_by("add_time")
        paginator = Paginator(content, 15)  # 分页对象
        contacts = paginator.get_page(page)
        return render(request, "product/list.html",
                      {"sort": sort,
                       "name": name,
                       "contacts": contacts,
                       })

    def post(self, request):
        return render(request, "", {})


# 分类页/二级分类
class CategoryView(View):
    def get(self, request, name):
        page = request.GET.get("page", "")
        # 排序方式
        sort = request.GET.get("sort", "")
        if not sort:
            sort = "default"
        if not page:
            page = 1
        content = TagAndProduct.objects.filter(tag__father__slug=name).all().order_by("add_time")
        paginator = Paginator(content, 15)  # 分页对象
        contacts = paginator.get_page(page)
        return render(request, "product/list.html",
                      {"sort": sort,
                       "name": name,
                       "contacts": contacts,
                       })

    def post(self, request):
        return render(request, "", {})


# 分类页/三级分类
class TagView(View):
    def get(self, request, name):
        page = request.GET.get("page", "")
        # 排序方式
        sort = request.GET.get("sort", "")
        if not sort:
            sort = "default"
        if not page:
            page = 1
        content = TagAndProduct.objects.filter(tag__slug=name).all().order_by("add_time")
        paginator = Paginator(content, 15)  # 分页对象
        contacts = paginator.get_page(page)
        return render(request, "product/list.html",
                      {"sort": sort,
                       "name": name,
                       "contacts": contacts,
                       })

    def post(self, request):
        return render(request, "", {})


# 详情页
class DetailView(View):
    def get(self, request, product_id):
        content = Product.objects.filter(id=product_id).first()
        # 点击数 + 1
        content.click_nums += 1
        return render(request, "product/detail.html",
                      {
                          "content": content,
                      })

    def post(self, request):
        return render(request, "", {})
