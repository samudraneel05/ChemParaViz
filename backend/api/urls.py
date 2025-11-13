from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'datasets', views.DatasetViewSet, basename='dataset')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('upload/', views.upload_dataset, name='upload'),
    path('datasets-list/', views.get_datasets, name='datasets-list'),
    path('dataset/<int:dataset_id>/', views.get_dataset_detail, name='dataset-detail'),
    path('dataset/<int:dataset_id>/delete/', views.delete_dataset, name='dataset-delete'),
    path('dataset/<int:dataset_id>/report/', views.generate_report, name='generate-report'),
    path('history/', views.get_history, name='history'),
]
