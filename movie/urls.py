from rest_framework import routers

from .views import MovieViewSet , TopMovieViewSet

routers = routers.DefaultRouter()
routers.register(r'movies', MovieViewSet, basename='movie')
routers.register(r'top-movies', TopMovieViewSet, basename='top-movie')


urlpatterns = routers.urls
