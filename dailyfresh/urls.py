"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include(blog_urls))
"""
from django.urls import re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')), # 富文本编辑器
    re_path(r'^search', include('haystack.urls')), # 全文检索框架
    re_path(r'^user/', include('user.urls', namespace='user')), # 用户模块
    re_path(r'^cart/', include('cart.urls', namespace='cart')), # 购物车模块
    re_path(r'^order/', include('order.urls', namespace='order')), # 订单模块
    re_path(r'^', include('goods.urls', namespace='goods')), # 商品模块
]

# 开发环境提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
