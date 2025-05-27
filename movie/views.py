from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
import os

from .serializers import MovieSerializer
from .models import Movie
from api.models import Category, Country, Topic
from actor.models import Actor
from web_movie_api.pagination import CustomPagination

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # ['title', 'slug', 'actor__slug' , 'category__slug' , 'country__slug' , 'topic__slug']
    search_fields = ['title', 'slug', 'actor__slug' , 'category__slug' , 'country__slug' , 'topic__slug']
    pagination_class = CustomPagination
    
    def get_permissions(self):
        if self.action in ['update', 'destroy', 'post']:
            return [permissions.AllowAny()]
        return [permissions.AllowAny()]

    def handle_many_to_many(self, instance, field_name, model, data):
        """Cập nhật mối quan hệ ManyToMany."""
        ids = data.get(field_name, [])
        if isinstance(ids, str):
            ids = [int(id) for id in ids.split(',')]
        elif isinstance(ids, list):
            ids = [int(id) for id in ids]
        related_objects = model.objects.filter(id__in=ids)
        getattr(instance, field_name).set(related_objects)

    def handle_foreign_key(self, instance, field_name, model, data):
        """Cập nhật mối quan hệ ForeignKey."""
        field_id = data.get(field_name)
        if field_id:
            related_object = get_object_or_404(model, id=field_id)
            setattr(instance, field_name, related_object)

    def delete_files(self, instance, fields):
        """Xóa các tệp liên quan đến bản ghi."""
        for field in fields:
            file_field = getattr(instance, field, None)
            if file_field and os.path.exists(file_field.path):
                os.remove(file_field.path)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            self.handle_many_to_many(instance, 'category', Category, data)
            self.handle_many_to_many(instance, 'actor', Actor, data)
            self.handle_many_to_many(instance, 'topic', Topic, data)
            self.handle_foreign_key(instance, 'country', Country, data)
            instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        # Xóa các tệp cũ nếu có
        self.delete_files(instance, ['image', 'image_avatar', 'video'])

        # Cập nhật các trường thông thường
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Cập nhật mối quan hệ ManyToMany và ForeignKey
        self.handle_many_to_many(instance, 'category', Category, data)
        self.handle_many_to_many(instance, 'actor', Actor, data)
        self.handle_many_to_many(instance, 'topic', Topic, data)
        self.handle_foreign_key(instance, 'country', Country, data)

        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        ids_to_delete = request.data.get("ids", [])
        if not ids_to_delete or not isinstance(ids_to_delete, list):
            return Response({"error": "Invalid or missing 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        existing_movies = Movie.objects.filter(id__in=ids_to_delete)
        existing_ids = list(existing_movies.values_list('id', flat=True))
        non_existing_ids = set(ids_to_delete) - set(existing_ids)

        if non_existing_ids:
            return Response(
                {"error": f"The following IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                for movie in existing_movies:
                    self.delete_files(movie, ['image', 'image_avatar', 'video'])
                existing_movies.delete()
            return Response({"message": f"Successfully deleted {len(existing_ids)} records"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='get-movies-header', permission_classes=[permissions.AllowAny])
    def get_movies_header(self, request):
        movies = Movie.objects.filter(is_banner=True)[:6]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='get-movies-ads', permission_classes=[permissions.AllowAny])
    def get_movies_ads(self, request):
        movies = Movie.objects.filter(is_ads=True)[:6]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='get-suggestion-movie', permission_classes=[permissions.AllowAny])
    def get_suggestion_movies(self, request):
        self.pagination_class = None
        if "actor" in request.query_params :
            actor_slug = request.query_params.get('actor', '').split(',')
            movies = Movie.objects.filter(actor__slug__in=actor_slug).distinct()
        elif "topic" in request.query_params :
            topic_slug = request.query_params.get('topic', '').split(',')
            movies = Movie.objects.filter(topic__slug__in=topic_slug).distinct()
        elif "category" in request.query_params :
            category_slug = request.query_params.get('category', '').split(',')
            movies = Movie.objects.filter(category__slug__in=category_slug).distinct()
        elif "country" in request.query_params :
            country_slug = request.query_params.get('country', '').split(',')
            movies = Movie.objects.filter(country__slug__in=country_slug).distinct()
        else:
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data if len(serializer.data) < 10 else serializer.data[:10], status=status.HTTP_200_OK)