# from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateAccountSerializer

# Create your views here.

@require_http_methods(["GET","POST"])
def hello_world(request):
    """Function printing python version."""
    return HttpResponse(content="OK")


class CreateAccountView(APIView):
    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)