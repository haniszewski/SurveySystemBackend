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