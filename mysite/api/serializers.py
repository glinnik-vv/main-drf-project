from .models import Post, Category, UploadFile, Patient, Direction, OrderInfo, Results, Measurement, Lpu
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


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


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer): 
    class Meta:
        model = OrderInfo
        fields = '__all__'



class ResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Results
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = '__all__'


class LpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lpu
        fields = '__all__'
