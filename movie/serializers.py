from rest_framework import serializers
from .models import Movie
from api.models import Category, Country, Topic
from actor.models import Actor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  # Chỉ định các trường bạn muốn serialize


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name' , 'image']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title']


class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)  # Serialize danh sách category
    country = CountrySerializer(read_only=True)  # Serialize country
    actor = ActorSerializer(many=True, read_only=True)  # Serialize danh sách actor
    topic = TopicSerializer(many=True, read_only=True)  # Serialize danh sách topic

    class Meta:
        model = Movie
        fields = '__all__'  # Hoặc chỉ định các trường cụ thể mà bạn muốn serialize