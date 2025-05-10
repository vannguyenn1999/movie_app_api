from django.shortcuts import render
from rest_framework import viewsets, permissions , status
from rest_framework.response import Response
from django.utils import timezone   
from django.db import transaction

import os

from .serializers import MovieSerializer
from .models import Movie
from api.models import Category, Country, Topic
from actor.models import Actor

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ['title']

    def get_object(self):
        return super().get_object()
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        
        # xóa ảnh cũ nếu có
        if 'image' in data:
            if instance.image: 
                image_path = instance.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)

        # Cập nhật các trường thông thường
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Cập nhật mối quan hệ ManyToMany (category, actor, topic)
        if 'category' in data:
            category_ids = data.get('category', [])
            
            if isinstance(category_ids, str):
                category_ids = [int(id) for id in category_ids.split(',')]
            elif isinstance(category_ids, list):
                category_ids = [int(id) for id in category_ids]
                
            categories = Category.objects.filter(id__in=category_ids)
            instance.category.set(categories)  # Cập nhật danh sách category

        if 'actor' in data:
            actor_ids = data.get('actor', [])
            
            if isinstance(actor_ids, str):
                actor_ids = [int(id) for id in actor_ids.split(',')]
            elif isinstance(actor_ids, list):
                actor_ids = [int(id) for id in actor_ids]
                
            actors = Actor.objects.filter(id__in=actor_ids)
            instance.actor.set(actors)  # Cập nhật danh sách actor

        if 'topic' in data:
            topic_ids = data.get('topic', [])
            
            if isinstance(topic_ids, str):
                topic_ids = [int(id) for id in topic_ids.split(',')]
            elif isinstance(topic_ids, list):
                topic_ids = [int(id) for id in topic_ids]
                
            topics = Topic.objects.filter(id__in=topic_ids)
            instance.topic.set(topics)  # Cập nhật danh sách topic

        # Cập nhật mối quan hệ ForeignKey (country)
        if 'country' in data:
            country_id = data.get('country')
            if country_id:
                country = get_object_or_404(Country, id=country_id)
                instance.country = country
                instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        ids_to_delete = request.data.get("ids", [])  # Nhận danh sách ID từ request
        if not ids_to_delete or not isinstance(ids_to_delete, list):
            return Response({"error": "Invalid or missing 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        existing_movies = Movie.objects.filter(id__in=ids_to_delete)
        # Lấy danh sách các ID thực sự tồn tại trong cơ sở dữ liệu
        existing_ids = list(Movie.objects.filter(id__in=ids_to_delete).values_list('id', flat=True))
        non_existing_ids = set(ids_to_delete) - set(existing_ids)

        if non_existing_ids:
            return Response(
                {"error": f"The following IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():  # Đảm bảo tính toàn vẹn dữ liệu
                for movie in existing_movies:
                    if movie.image: 
                        image_path = movie.image.path
                        if os.path.exists(image_path):
                            os.remove(image_path)
                
                # Xóa tất cả các bản ghi có ID trong danh sách
                existing_movies.delete()
            return Response({"message": f"Successfully deleted {len(existing_ids)} records"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


