from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny 
from rest_framework.views import APIView

import pytz , os

from .serializers import CustomTokenObtainPairSerializer , CustomTokenRefreshSerializer
from .models import NewUser


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)        
         # Lấy thông tin người dùng từ email
        user = NewUser.objects.get(email=request.data['email'])
         # Cập nhật trường last_login theo múi giờ Việt Nam
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        user.last_login = timezone.now().astimezone(vietnam_tz)
        user.save()

        return Response({
            'message': 'Login successful',
            'data': response.data
        }, status=status.HTTP_200_OK)

# Lấy token mới khi token cũ bị hết hạn
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    
class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)