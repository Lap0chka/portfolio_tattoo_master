from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh_captcha/', views.refresh_captcha, name='refresh_captcha'),
    path('about/', views.about_me, name='about'),
    path('portfolio/', views.portfolio, name='porfolio'),
    path('information/', views.information, name='information'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('post/<slug:post>/', views.post_deteil, name='post_detail'),
]
