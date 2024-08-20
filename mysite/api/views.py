from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer
from .models import Post, Category
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import LimitOffsetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination 

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
