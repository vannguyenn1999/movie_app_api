from rest_framework import serializers
from .models import Movie , TopMovie
from api.models import Category, Country, Topic
from actor.models import Actor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name' , 'slug']  # Chỉ định các trường bạn muốn serialize


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name' , 'slug']  # Chỉ định các trường bạn muốn serialize


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name' , 'image' , 'slug']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title' , 'slug']


class MovieSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)  # Serialize danh sách category
    country = CountrySerializer(read_only=True)  # Serialize country
    actor = ActorSerializer(many=True, read_only=True)  # Serialize danh sách actor
    topic = TopicSerializer(many=True, read_only=True)  # Serialize danh sách topic

    class Meta:
        model = Movie
        fields = '__all__'  # Hoặc chỉ định các trường cụ thể mà bạn muốn serialize
        
class TopMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = TopMovie
        fields = '__all__' 