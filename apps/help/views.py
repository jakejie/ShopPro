from django.shortcuts import render
from django.views.generic.base import View


# 帮助中心
class HelpCenView(View):
    def get(self, request):
        return render(request, "", {})

    def post(self, request):
        return render(request, "", {})
