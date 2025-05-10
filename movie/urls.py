from rest_framework import routers

from .views import MovieViewSet

routers = routers.DefaultRouter()
routers.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = routers.urls
