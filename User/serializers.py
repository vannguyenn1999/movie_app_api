
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer , TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import NewUser


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Get default token data
        user = self.user  # Lấy thông tin user từ token
        request = self.context.get('request')
        if user.image:
            image_url = request.build_absolute_uri(user.image.url) if user.image else None
        else:
            image_url = None
        data['user'] = {
            'id': user.id,
            'username': user.user_name,
            'email': user.email,
            'image' : image_url,
            'is_staff' : user.is_staff
        }

        return data
    

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Lấy thông tin người dùng từ refresh token
        refresh = self.token_class(attrs['refresh'])
        user_id = refresh['user_id']
        user = NewUser.objects.get(id=user_id)
        new_refresh = RefreshToken.for_user(user)
        refresh.blacklist()
        # Thêm thông tin người dùng vào phản hồi
        request = self.context.get('request')
        image_url = request.build_absolute_uri(user.image.url) if user.image else None
        data['refresh'] = str(new_refresh)
        data['access'] = str(new_refresh.access_token)
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.user_name,
            'image': image_url,
            'is_staff': user.is_staff,
        }
        
        return data