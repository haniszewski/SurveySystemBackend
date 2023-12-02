from rest_framework import permissions
from controllers.models import SurveyOwners

class IsSurveyCreator(permissions.BasePermission):
    message = 'Not creator'
    def has_permission(self, request, view):
        survey_id = view.kwargs.get('survey_id', None)
        if survey_id is not None:
            return SurveyOwners.objects.filter(user=request.user, survey__id=survey_id,permissions__id = 1).exists()
        return False

class IsSurveyOwner(permissions.BasePermission):
    message = 'Not owner'
    def has_permission(self, request, view):
        survey_id = view.kwargs.get('survey_id', None)
        if survey_id is not None:
            return SurveyOwners.objects.filter(user=request.user, survey__id=survey_id,permissions__id = 2).exists()
        return False

class IsSurveyEditor(permissions.BasePermission):
    message = 'Not editor'
    def has_permission(self, request, view):
        survey_id = view.kwargs.get('survey_id', None)
        if survey_id is not None:
            return SurveyOwners.objects.filter(user=request.user, survey__id=survey_id, permissions__id = 3).exists()
        return False

class IsSurveyViewer(permissions.BasePermission):
    message = 'Not viewer'
    def has_permission(self, request, view):
        survey_id = view.kwargs.get('survey_id', None)
        if survey_id is not None:
            return SurveyOwners.objects.filter(user=request.user, survey__id=survey_id, permissions__id = 4).exists()
        return False