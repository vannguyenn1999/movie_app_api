from rest_framework import viewsets 
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction


from .models import Topic, Category, Country
from .serializers import TopicSerializer, CategorySerializer, CountrySerializer


class BaseModelViewSet(viewsets.ModelViewSet):
    pagination_class = None

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [AllowAny()]
            return [IsAuthenticated()]
        return [AllowAny()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_at = timezone.now()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        ids_to_delete = request.data.get("ids", [])
        if not isinstance(ids_to_delete, list) or not ids_to_delete:
            return Response({"error": "Invalid or missing 'ids' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        existing_ids = list(self.queryset.model.objects.filter(id__in=ids_to_delete).values_list('id', flat=True))
        non_existing_ids = set(ids_to_delete) - set(existing_ids)

        if non_existing_ids:
            return Response(
                {"error": f"The following IDs do not exist: {list(non_existing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                self.queryset.model.objects.filter(id__in=existing_ids).delete()
            return Response({"message": f"Successfully deleted {len(existing_ids)} records"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TopicViewSet(BaseModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

class CategoryViewSet(BaseModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CountryViewSet(BaseModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
