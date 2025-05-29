from django.shortcuts import render
from rest_framework import viewsets, permissions , status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django.db import models

import os

from .serializers import ActorSerializer
from .models import Actor
from web_movie_api.pagination import CustomPagination

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['name' , 'slug']
    pagination_class = CustomPagination

    # def get_permissions(self):
    #     if self.action == 'update' or self.action == 'destroy':
    #         return [IsAuthenticated()]
    #     return [AllowAny()]
    
    def get_object(self):
        return super().get_object()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            keywords = [kw.strip() for kw in search.split(',') if kw.strip()]
            q = models.Q()
            for kw in keywords:
                q |= models.Q(name__icontains=kw) | models.Q(slug__icontains=kw)                
            queryset = queryset.filter(q).distinct()
        return queryset
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        instance.updated_at = timezone.now()
        if "image" in data:
            if instance.image: 
                image_path = instance.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance,  data=data , partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        ids_to_delete = request.data.get("ids", [])  # Nhận danh sách ID từ request
        if not ids_to_delete or not isinstance(ids_to_delete, list):
            return Response({"error": "Invalid or missing 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        existing_actors = Actor.objects.filter(id__in=ids_to_delete)
        # Lấy danh sách các ID thực sự tồn tại trong cơ sở dữ liệu
        existing_ids = list(Actor.objects.filter(id__in=ids_to_delete).values_list('id', flat=True))
        non_existing_ids = set(ids_to_delete) - set(existing_ids)

        if non_existing_ids:
            return Response(
                {"error": f"The following IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():  # Đảm bảo tính toàn vẹn dữ liệu
                for actor in existing_actors:
                    if actor.image: 
                        image_path = actor.image.path
                        if os.path.exists(image_path):
                            os.remove(image_path)
                
                # Xóa tất cả các bản ghi có ID trong danh sách
                existing_actors.delete()
            return Response({"message": f"Successfully deleted {len(existing_ids)} records"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
