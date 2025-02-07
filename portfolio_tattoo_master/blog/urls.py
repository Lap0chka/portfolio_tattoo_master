from . import views
from django.urls import path

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<slug:slug>', views.detail_post, name='post_detail'),
]
