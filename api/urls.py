from rest_framework.routers import DefaultRouter

from .views import TopicViewSet, CategoryViewSet, CountryViewSet

router = DefaultRouter()

router.register(r'topics', TopicViewSet, basename='topics')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'countries', CountryViewSet, basename='countries')


urlpatterns = router.urls