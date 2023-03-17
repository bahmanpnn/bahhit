from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class VoteCreate(CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('you have already voted for this post!!')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs.get('pk')))
