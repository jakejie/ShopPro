from django.urls import path
from .views import PayView, CheckPayStatusView

urlpatterns = [
    path('', PayView.as_view(), name="pay"),
    path('check_pay/', CheckPayStatusView.as_view(), name="check_pay"),
]
