from django.shortcuts import render
from typing import Dict, Any
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .serializers_auth import *
from controllers.models import SystemUser
from django.db import transaction


class CreateUserView(APIView):
    def post(self, request, format=None):
        serializer = SystemUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)