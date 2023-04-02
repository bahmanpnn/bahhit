from django.urls import path
from .views import *

urlpatterns = [
    path('posts-list/', PostList.as_view(), name='posts-list'),
    path('posts-list/<int:pk>/', PostRetrieveDestroy.as_view(), name='post-page'),
    path('posts-list/<int:pk>/vote', VoteCreate.as_view(), name='vote-post'),
]
