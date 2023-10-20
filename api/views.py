# from django.shortcuts import render
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateAccountSerializer
from django.contrib.auth.models import User

# Create your views here.

@require_http_methods(["GET","POST"])
def hello_world(request):
    """Function printing python version."""
    return HttpResponse(content="OK")


class CreateAccountView(APIView):
    def put(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"detail": "Email already exists."}, status=status.HTTP_409_CONFLICT)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
      
class CreateSurveyView(APIView):
    def put(self,request):
        return HttpResponse("ok")
    
class ReadSurveyView(APIView):
    def post(self,request):
        return HttpResponse("ok")