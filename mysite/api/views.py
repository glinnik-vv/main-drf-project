from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post
from .permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)
