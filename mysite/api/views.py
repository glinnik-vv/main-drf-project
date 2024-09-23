from datetime import datetime
import os
from django.forms import ValidationError
import pandas as pd
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PostSerializer, CategorySerializer, UploadFileSerializer, PatientSerializer, DirectionSerializer, OrderInfoSerializer, ResultsSerializer, MeasurementSerializer, LpuSerializer
from .models import Post, Category, UploadFile, Patient, Direction, OrderInfo, Results, Measurement, Lpu
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PatientFilter


def import_patients_from_excel(file_path):
    # Читаем данные из файла Excel
    data = pd.read_excel(file_path)

    # Проходим по строкам и создаем объекты Patient
    for _, row in data.iterrows():
        Patient.objects.create(
            first_name=row['first_name'],
            last_name=row['last_name'],
            age=row['age'],
            # добавьте другие поля по необходимости
        )


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientFilter


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination 

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('created_at')
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
        
        # Проверка расширения файла
        valid_extensions = ['.xls', '.xlsx']
        file_extension = os.path.splitext(file.name)[1]
        if file_extension not in valid_extensions:
            raise ValidationError('Недопустимое расширение файла')

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = f'{folder_path}/{file.name}'
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        
        serializer.save(file=file_path, service_name=service_name)
        
        # Импортируем данные из файла Excel
        import_patients_from_excel(file_path)


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class OrderInfoViewSet(viewsets.ModelViewSet):
    queryset = OrderInfo.objects.all()
    serializer_class = OrderInfoSerializer


class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Results.objects.all()
    serializer_class = ResultsSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class LpuViewSet(viewsets.ModelViewSet):
    queryset = Lpu.objects.all()
    serializer_class = LpuSerializer
