from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)


class PostRetrieveDestroy(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)

    def delete(self, request, *args, **kwargs):
        target_post = Post.objects.filter(pk=self.kwargs['pk'], poster=self.request.user)
        if target_post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('you don\'t have permission to delete this post!')


class VoteCreate(CreateAPIView, DestroyModelMixin):
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

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('you didnt voted this post!!')
