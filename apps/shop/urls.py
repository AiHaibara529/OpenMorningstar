from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.index, name='index'),
]