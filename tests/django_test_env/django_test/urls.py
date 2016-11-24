# -*- coding: utf-8 -*-
"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from werobot import WeRoBot
from werobot.contrib.django import make_view
from werobot.utils import generate_token

robot = WeRoBot(enable_session=False,
                token="TestDjango",
                app_id="9998877",
                encoding_aes_key=generate_token(32))


@robot.text
def text_handler():
    return 'hello'


@robot.error_page
def make_error_page(url):
    return '喵'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^robot/', make_view(robot))
]
