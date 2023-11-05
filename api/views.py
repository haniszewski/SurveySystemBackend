from django.shortcuts import render
from typing import Dict, Any
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.contrib.auth.models import User
from django.db import transaction



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
    
    def post(self, request, *args, **kwargs):
        serializer = SurveySerializer(data=request.data)
        if serializer.is_valid():
            # Start Database transaction
            with transaction.atomic():
                survey = Survey.objects.create(
                    name=serializer.validated_data['name'],
                    start_date=serializer.validated_data['start_date'],
                    end_date=serializer.validated_data['end_date']
                )
                for form_data in serializer.validated_data['forms']:
                    form_input = FormInput.objects.create(
                        survey=survey,
                        question_type=form_data['question_type'],
                        order=form_data['order'],
                        question_text=form_data['question_text']
                    )
                    
                    # If choices empty throw error
                    for choice_data in form_data['choices']:
                        FormInputChoice.objects.create(
                            form=form_input,
                            option_text=choice_data['option_text']
                        )
                
                # TODO add current user as owner of survey
                # SurveyOwners.objects.create(user=request.user, survey=survey)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllSurveyByOwnerView(APIView):
    def get(self,request):
        return HttpResponse("ok")
    
class ReadSurveyView(APIView):
    def post(self,request):
        return HttpResponse("ok")