
from django.urls import path

from .views import BlacklistTokenUpdateView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/' , CustomTokenRefreshView.as_view()),
    path('auth/logout/blacklist/', BlacklistTokenUpdateView.as_view(), name='blacklist'),
]