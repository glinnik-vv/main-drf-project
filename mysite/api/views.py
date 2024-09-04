from datetime import datetime
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer, UploadFileSerializer
from .models import Post, Category, UploadFile
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


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer

    def perform_create(self, serializer):
        file = serializer.validated_data['file']
        service_name = serializer.validated_data['service_name']
        current_date = datetime.now().strftime('%Y-%m-%d')
        folder_path = f'uploads/{current_date}/{service_name}'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = f'{folder_path}/{file.name}'
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        serializer.save(file=file_path, service_name=service_name)
