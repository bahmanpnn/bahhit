from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Post
from .serializers import PostSerializer


class PostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
