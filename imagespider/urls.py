from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
        url(r'^sp$',views.spider_view),
]