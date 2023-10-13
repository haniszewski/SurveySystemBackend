# from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http.response import HttpResponse

# Create your views here.

def hello_world(request):
    """Function printing python version."""
    return HttpResponse(content="OK")

# def login(request):
#     return HttpResponse(content="Logged in")

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['name'] = user.name
        # ...

        return token