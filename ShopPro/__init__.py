import pymysql
from .celery import app as celery_app

pymysql.install_as_MySQLdb()

# 这将保证celery app 总能在django应用启动时启动

__all__ = ['celery_app']
