from django.urls import path
from .views import *

urlpatterns = [
    path('posts-list/', PostList.as_view(), name='posts-list'),
    path('posts-list/<int:pk>/vote', VoteCreate.as_view(), name='vote-post'),
]
