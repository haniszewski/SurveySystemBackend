from django.shortcuts import render
from typing import Dict, Any
from django.db import IntegrityError
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated

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


 
# class CreateAccountView(APIView):
#     def put(self, request):
#         serializer = CreateAccountSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 user = serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except IntegrityError:
#                 return Response({"detail": "Email already exists."}, status=status.HTTP_409_CONFLICT)
            
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateSurveyView(APIView):
    # permission_classes = [IsAuthenticated]    
    
    def post(self, request, *args, **kwargs):
        serializer = SurveyCreateSerializer(data=request.data)
        user = SystemUser.objects.get(id = 1)
        # user = request.user
        if serializer.is_valid():
            # Start Database transaction
            with transaction.atomic():
                survey = Survey.objects.create(
                    name=serializer.validated_data['name'], # type: ignore
                    start_date=serializer.validated_data['start_date'], # type: ignore
                    end_date=serializer.validated_data['end_date'], # type: ignore
                    status = SurveyStatus.objects.get(id=1)
                )
                for form_data in serializer.validated_data['questions']: # type: ignore
                    form_input = FormInput.objects.create(
                        survey=survey,
                        type=form_data['type'],
                        order=form_data['order'],
                        text=form_data['text']
                    )
                    
                    # If choices empty throw error
                    for choice_data in form_data['choices']:
                        FormInputChoice.objects.create(
                            input=form_input,
                            text=choice_data['text'],
                            order=choice_data['order']
                        )                
                # TODO add current user as owner of survey
                permission = SurveyPermissions.objects.get(id=1)
                SurveyOwners.objects.create(user=user, survey=survey, permissions=permission)
                
            response_data = serializer.data
            response_data['id'] = survey.id # type: ignore
                
            return Response(response_data, status=status.HTTP_201_CREATED)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllSurveyByOwnerView(APIView):
    def get(self,request):
        return HttpResponse("ok")
    
class ReadSurveyView(APIView):
    def post(self,request):
        return HttpResponse("ok")
    
    
class SurveyGetView(APIView):
    def get(self, request, pk):
        try:
            survey = Survey.objects.get(pk=pk)
            serializer = SurveyGetSerializer(survey)
            return Response(serializer.data)
        except Survey.DoesNotExist:
            return Response({'error': 'Survey not found'}, status=status.HTTP_404_NOT_FOUND)
        
class AnswerSubmissionView(APIView):
    def post(self, request, survey_id):
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            return Response({'error': 'Survey not found'}, status=status.HTTP_404_NOT_FOUND)

        questions = FormInput.objects.filter(survey=survey)
        if 'answers' not in request.data or len(request.data['answers']) != questions.count():
            return Response({'error': 'Answers for all questions are required'}, status=status.HTTP_400_BAD_REQUEST)

        responses = []
        for answer_data in request.data['answers']:
            serializer = AnswerSubmissionSerializer(data=answer_data)
            if serializer.is_valid():
                serializer.save()
                responses.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(responses, status=status.HTTP_201_CREATED)