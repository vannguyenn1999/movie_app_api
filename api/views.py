from rest_framework import viewsets 
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction


from .models import Topic, Category, Country
from .serializers import TopicSerializer, CategorySerializer, CountrySerializer


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    # permission_classes = [AllowAny]  # Allow any user to access this viewsetAllowAny
    queryset = Topic.objects.all()
    pagination_class = None  
    
    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_object(self):
        return super().get_object()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        instance.updated_at = timezone.now()  # Cập nhật thời gian hiện tại
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance,  data=data , partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        ids_to_delete = request.data.get("ids", [])  # Nhận danh sách ID từ request
        if not ids_to_delete or not isinstance(ids_to_delete, list):
            return Response({"error": "Invalid or missing 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy danh sách các ID thực sự tồn tại trong cơ sở dữ liệu
        existing_ids = list(Topic.objects.filter(id__in=ids_to_delete).values_list('id', flat=True))
        non_existing_ids = set(ids_to_delete) - set(existing_ids)

        if non_existing_ids:
            return Response(
                {"error": f"The following IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():  # Đảm bảo tính toàn vẹn dữ liệu
                # Xóa tất cả các bản ghi có ID trong danh sách
                Topic.objects.filter(id__in=existing_ids).delete()
            return Response({"message": f"Successfully deleted {len(existing_ids)} records"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    # permission_classes = [AllowAny]
    queryset = Category.objects.all()
    pagination_class = None  
    
    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_object(self):
        return super().get_object()
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        instance.updated_at = timezone.now()  # Cập nhật thời gian hiện tại
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance,  data=data , partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def destroy(self, request, *args, **kwargs):
        ids_to_delete = request.data.get("ids", [])
        if not ids_to_delete or not isinstance(ids_to_delete, list):
            return Response({"error": "Invalid or missing 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Lấy danh sách các ID thực sự tồn tại trong cơ sở dữ liệu
        existing_ids = list(Category.objects.filter(id__in=ids_to_delete).values_list('id', flat=True))
        non_existing_ids = set(ids_to_delete) - set(existing_ids)
        
        if non_existing_ids:
            return Response(
                {"error": f"The following IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            with transaction.atomic():  # Đảm bảo tính toàn vẹn dữ liệu
                # Xóa tất cả các bản ghi có ID trong danh sách
                Category.objects.filter(id__in=existing_ids).delete()
            return Response({"message": f"Successfully deleted {len(existing_ids)} records"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    pagination_class = None  
    def get_permissions(self):
        if self.action == 'update' or self.action == 'destroy':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_object(self):
        return super().get_object()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        instance.updated_at = timezone.now()  # Cập nhật thời gian hiện tại
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance,  data=data , partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        ids_to_delete = request.data.get("ids", [])  # Nhận danh sách ID từ request
        if not ids_to_delete or not isinstance(ids_to_delete, list):
            return Response({"error": "Invalid or missing 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy danh sách các ID thực sự tồn tại trong cơ sở dữ liệu
        existing_ids = list(Country.objects.filter(id__in=ids_to_delete).values_list('id', flat=True))
        non_existing_ids = set(ids_to_delete) - set(existing_ids)

        if non_existing_ids:
            return Response(
                {"error": f"The following IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():  # Đảm bảo tính toàn vẹn dữ liệu
                # Xóa tất cả các bản ghi có ID trong danh sách
                Country.objects.filter(id__in=existing_ids).delete()
            return Response({"message": f"Successfully deleted {len(existing_ids)} records"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

