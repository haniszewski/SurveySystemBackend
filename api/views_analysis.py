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
from rest_framework.permissions import IsAuthenticated
from controllers.models import SystemUser
from django.db import transaction
from .permissions import *
from .serializers_analysis import *
from .analysis_functions import *


class AddUpdateSurveyAnalysis(APIView):
    permission_classes = [IsAuthenticated, IsSurveyCreator] 

    def post(self, request, survey_id, format=None):
        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            return Response({'error': 'Survey not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AnalysisSchemaSerializer(data=request.data)
        if serializer.is_valid():
            survey.analysis_json = serializer.validated_data['analysis_schema'] # type: ignore
            survey.save()
            return Response({'message': 'Analysis schema updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RunSurveyAnalysis(APIView):
    permission_classes = [IsAuthenticated, IsSurveyCreator]
    def post(self, request, survey_id, format=None):
        try:
            analyze_survey(survey_id)
            return Response({'message': 'Survey analysis completed successfully'}, status=status.HTTP_200_OK)
        except Survey.DoesNotExist:
            return Response({'error': 'Survey not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
class GetAnalysisResult(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, survey_id, format=None):
        try:
            survey = Survey.objects.get(pk=survey_id)
            return Response({'analysis_result_json': survey.analysis_result_json}, status=status.HTTP_200_OK)
        except Survey.DoesNotExist:
            return Response({'error': 'Survey not found'}, status=status.HTTP_404_NOT_FOUND)