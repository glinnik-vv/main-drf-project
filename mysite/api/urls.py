from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CategoryViewSet, UploadFileViewSet, PatientViewSet, DirectionViewSet, OrderInfoViewSet, ResultsViewSet, MeasurementViewSet, LpuViewSet
from rest_framework.authtoken import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register('posts', PostViewSet)
router.register('categories', CategoryViewSet)
router.register('patients', PatientViewSet)
router.register('directions', DirectionViewSet)
router.register('orderinfo', OrderInfoViewSet)
router.register('results', ResultsViewSet)
router.register('measurements', MeasurementViewSet)
router.register('lpu', LpuViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', UploadFileViewSet.as_view({'post': 'create'}), name='file-upload'),
]
