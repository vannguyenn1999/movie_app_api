from rest_framework import serializers

from .models import Actor


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
        # read_only_fields = ['slug', 'created_at', 'updated_at']