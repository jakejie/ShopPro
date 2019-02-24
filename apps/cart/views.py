import uuid
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from .models import CartProduct


# 我的购物车 ok
class CartView(View):
    # 我的购物车
    def get(self, request):
        # 获取购物车中的所有商品
        if request.user.is_authenticated:
            return render(request, "cart/cart.html", )

        else:
            return redirect(reverse('index'))

    # 在购物车页 去结算
    def post(self, request):
        if request.user.is_authenticated:
            target = uuid.uuid4()
            books = request.POST.get("books", "")
            print("收到商品ID：{} 生成UUID：{}".format(books.split(','), target))
            book_list = books.split(',')
            for book in book_list:
                if book:
                    product = CartProduct.objects.filter(
                        user_id=request.user.id, product_id=int(book)).first()
                    product.commit_target = target
                    product.save()
            data = {
                "code": 3,
                "msg": "正常 跳转",
                "target": target
            }
            # return redirect(reverse("commit"))
            # return render(request, 'order/place_order.html',)
        else:
            data = {
                "code": 2,
                "msg": "异常 错误"
            }
        return JsonResponse(data)


# 加入购物车 ok
class CartAddView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        if request.user.is_authenticated:
            books_id = request.POST.get("books_id")
            books_count = request.POST.get("books_count")
            cart = CartProduct.objects.filter(
                user_id=request.user.id,
                product_id=books_id).first()
            if cart:
                cart.num = cart.num + int(books_count)
                cart.save()
            else:
                cart = CartProduct(
                    user_id=int(request.user.id),
                    product_id=books_id,
                    num=int(books_count),
                )
                cart.save()
            data = {
                "code": 1,
                "msg": "加入成功"
            }
        else:
            data = {
                "code": 0,
                "msg": "您尚未登陆"
            }
        return JsonResponse(data)


# 从购物车中删除 ok
class CartDelView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        if request.user.is_authenticated:
            books_id = request.POST.get("books_id")
            print("删除商品：{}".format(books_id))
            cart = CartProduct.objects.filter(
                user_id=request.user.id, product_id=int(books_id)).delete()
            data = {
                "code": 3,
                "msg": "删除成功"
            }
        else:
            data = {
                "code": 0,
                "msg": "您尚未登陆"
            }
        return JsonResponse(data)


# 购物车数量同步 ok
class CartUpdateView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        if request.user.is_authenticated:
            books_id = request.POST.get("books_id", "")
            books_count = request.POST.get("books_count")
            # 更新数据库
            cart = CartProduct.objects.filter(
                user_id=request.user.id, product_id=int(books_id)).first()
            cart.num = int(books_count)
            cart.save()
            data = {
                "code": 3,
                "msg": "数量同步成功"
            }
        else:
            data = {
                "code": 0,
                "msg": "您尚未登陆"
            }
        return JsonResponse(data)


# 获取购物车中商品总数量 ok
class CartCountView(View):
    def get(self, request):
        if request.user.is_authenticated:
            count = 0
            product_list = CartProduct.objects.filter(user_id=request.user.id).all()
            for num in product_list:
                count += num.num
            data = {
                "code": 1,
                "msg": "获取总数成功",
                "cou": count
            }
        else:
            data = {
                "code": 0,
                "msg": "您尚未登陆"
            }
        return JsonResponse(data)

    def post(self, request):
        pass


# 清空购物车 暂时不需要
class EmptyCartView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})
