from rest_framework import serializers
from django.contrib.auth.models import User

class CreateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    login = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['login'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name'],
            last_name=validated_data['surname']
        )
        return user
    
    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'login': instance.username,
            'name': instance.first_name,
            'surname': instance.last_name,
        }