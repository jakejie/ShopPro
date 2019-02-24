import os
from celery import Celery

# 为celery程序设置Django settings module 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShopPro.settings')

# app = Celery('ShopPro', broker='redis://[:zhujie165102]@127.0.0.1:6379/6')
app = Celery('ShopPro', broker='redis://localhost:6379/6')
# 从Django的设置文件中导入celery设置
app.config_from_object('django.conf:settings', namespace="CELERY")  #
# 从所有已注册的app中加载任务模块
app.autodiscover_tasks()
