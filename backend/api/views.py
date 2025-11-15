from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from .models import Dataset, Equipment
from .serializers import (
    DatasetSerializer, 
    DatasetUploadSerializer,
    EquipmentSerializer,
    UserSerializer
)
from .utils import process_csv, get_dataset_summary
from .pdf_generator import generate_pdf_report


def index(request):
    """Landing page"""
    return render(request, 'index.html')


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'user': UserSerializer(user).data,
        'token': token.key
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """Login user and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'user': UserSerializer(user).data,
        'token': token.key
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_dataset(request):
    """Upload and process CSV dataset"""
    serializer = DatasetUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        file = serializer.validated_data['file']
        dataset = process_csv(file, request.user)
        
        return Response(
            DatasetSerializer(dataset).data,
            status=status.HTTP_201_CREATED
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_datasets(request):
    """Get all datasets for the authenticated user"""
    datasets = Dataset.objects.filter(user=request.user)
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, dataset_id):
    """Get detailed information about a specific dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        summary = get_dataset_summary(dataset)
        return Response(summary)
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    """Delete a dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        dataset.file.delete()
        dataset.delete()
        return Response(
            {'message': 'Dataset deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_report(request, dataset_id):
    """Generate PDF report for a dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        pdf_buffer = generate_pdf_report(dataset)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
        return response
    except Dataset.DoesNotExist:
        return Response(
            {'error': 'Dataset not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """Get upload history (last 5 datasets)"""
    datasets = Dataset.objects.filter(user=request.user)[:5]
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)


class DatasetViewSet(viewsets.ModelViewSet):
    """ViewSet for dataset CRUD operations"""
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get dataset summary"""
        dataset = self.get_object()
        summary = get_dataset_summary(dataset)
        return Response(summary)
    
    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Generate PDF report"""
        dataset = self.get_object()
        pdf_buffer = generate_pdf_report(dataset)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
        return response
