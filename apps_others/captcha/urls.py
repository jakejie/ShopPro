from django.conf.urls import url
from captcha import views
from django.urls import path

urlpatterns = [
    path('image/<key>/', views.captcha_image, name='captcha-image', kwargs={'scale': 1}),
    path('image/<key>/', views.captcha_image, name='captcha-image-2x', kwargs={'scale': 2}),
    path('audio/<key>', views.captcha_audio, name='captcha-audio'),
    path('refresh/', views.captcha_refresh, name='captcha-refresh'),
]

# urlpatterns = [
#     url(r'image/(?P<key>\w+)/$', views.captcha_image, name='captcha-image', kwargs={'scale': 1}),
#     url(r'image/(?P<key>\w+)@2/$', views.captcha_image, name='captcha-image-2x', kwargs={'scale': 2}),
#     url(r'audio/(?P<key>\w+).wav$', views.captcha_audio, name='captcha-audio'),
#     url(r'refresh/$', views.captcha_refresh, name='captcha-refresh'),
# ]
