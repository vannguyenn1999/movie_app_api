from rest_framework import serializers
from .models import Topic , Category , Country


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
        
    def validate_title(self, data):
        if data == "":
            raise serializers.ValidationError("Tiêu đề không được để trống")
        elif len(data) < 1:
            raise serializers.ValidationError("Tiêu đề phải lớn hơn 1 ký tự")
        elif len(data) > 20:
            raise serializers.ValidationError("Tiêu đề phải nhỏ hơn 20 ký tự")
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
    
    def validate_name(self, data):
        if data == "":
            raise serializers.ValidationError("Tên thể loại không được để trống")
        elif len(data) < 3:
            raise serializers.ValidationError("Tên thể loại phải lớn hơn 3 ký tự")
        elif len(data) > 20:
            raise serializers.ValidationError("Tên thể loại phải nhỏ hơn 20 ký tự")
        return data


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        
    def validate_name(self, data):
        if data == "":
            raise serializers.ValidationError("Tên quốc gia không được để trống")
        elif len(data) < 1:
            raise serializers.ValidationError("Tên quốc gia phải lớn hơn 1 ký tự")
        elif len(data) > 20:
            raise serializers.ValidationError("Tên quốc gia phải nhỏ hơn 20 ký tự")
        return data

