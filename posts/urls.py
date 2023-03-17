from django.urls import path
from .views import *

urlpatterns = [
    path('posts-list/', PostList.as_view(), name='posts-list')
]
