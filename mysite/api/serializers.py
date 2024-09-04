from .models import Post, Category, UploadFile
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UploadFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    service_name = serializers.CharField()

    class Meta:
        model = UploadFile
        fields = ('file', 'service_name')
