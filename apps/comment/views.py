from django.shortcuts import render
from django.views.generic.base import View


# 添加评论
class AddCommentView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 回复评论
class ReplyCommentView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})


# 查看评论
class CommentView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})
