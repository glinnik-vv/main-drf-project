from datetime import datetime
import os
from sshtunnel import SSHTunnelForwarder
from django.forms import ValidationError
from django.http import JsonResponse
from django.views import View
import pandas as pd
from rest_framework import viewsets
from sqlalchemy import URL, create_engine
from .serializers import UserSettingsSerializer, AppSettingsSerializer, PostSerializer, CategorySerializer, UploadFileSerializer, PatientSerializer, DirectionSerializer, OrderInfoSerializer, ResultsSerializer, MeasurementSerializer, LpuSerializer
from .models import UserSettings, AppSettings, Post, Category, UploadFile, Patient, Direction, OrderInfo, Results, Measurement, Lpu
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PatientFilter
  

def import_patients_from_excel(file_path):
    # Читаем данные из файла Excel
    data = pd.read_excel(file_path)

    # Создаем список объектов Patient
    patients = []
    for _, row in data.iterrows():
        patients.append(Patient(
            first_name=row['first_name'],
            last_name=row['last_name'],
            surname=row['surname'],
            id_pac=row['id_pac'],
            birth_date=row['birth_date'],
            sex=row['sex'],
            snils=row['snils'],
        ))
    # Обновляем существующие объекты Patient
    Patient.objects.bulk_create(patients, update_conflicts=True, update_fields=['first_name', 'last_name', 'surname', 'birth_date', 'sex', 'snils'])


class UserSettingsViewSet(viewsets.ModelViewSet):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer


class AppSettingsViewSet(viewsets.ModelViewSet):
    queryset = AppSettings.objects.all()
    serializer_class = AppSettingsSerializer


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


class ImportLpuDataView(View):
    def get(self, request):
        setting_name = 'ЦКДЛ'
        app_setting = AppSettings.objects.get(name=setting_name)
        
        db_params = {
            'database': app_setting.unigate_db_name,
            'user': app_setting.unigate_db_user,
            'password': app_setting.unigate_db_password,
            'host': app_setting.unigate_db_host,
            'port': app_setting.unigate_db_port
        }

        if setting_name != 'СО':
            # настройки SSH-сервера
            ssh_host = '10.10.40.4'
            ssh_port = 22
            ssh_username = 'eamk'
            ssh_password = 'QAZ12qaz'
            # создаем туннель
            tunnel = SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                remote_bind_address=(db_params['host'], int(db_params['port']))
            )
            # запускаем туннель
            tunnel.start()
            db_params['port'] = tunnel.local_bind_port
        
        url_obj = URL.create(
            'postgresql+psycopg2',
            username=db_params['user'],
            password=db_params['password'],
            host=db_params['host'],
            port=int(db_params['port']),
            database=db_params['database']
        )

        engine = create_engine(url_obj) 
        connection = engine.connect()

        df = pd.read_sql('SELECT "LpuId" code, "UserName" name, "UserPassword" unigate_login, "UnigateName" unigate_password FROM "CheckInfos"', connection)
        tunnel.close()
        lpus = []
        for index, row in df.iterrows():
            lpus.append(Lpu(
                code=row['code'],
                name=row['name'],
                unigate_login=row['unigate_login'],
                unigate_password=row['unigate_password']
            ))
        Lpu.objects.bulk_create(lpus, update_conflicts=True, update_fields=['name', 
                                                                            'unigate_login', 
                                                                            'unigate_password'], 
                                                                            unique_fields=['code'])

        return JsonResponse({'status': 'success', 
                             'message': 'LPU data imported successfully'})
