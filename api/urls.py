from django.urls import path
from rest_framework.schemas import get_schema_view

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views_auth import CreateUserView
from .views_analysis import *
from .views import hello_world, CreateSurveyView, ReadSurveyView, GetAllSurveyByOwnerView, SurveyGetView, AnswerSubmissionView

urlpatterns = [
    # ...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('docs', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('', view=hello_world),
    path('account/create/', view=CreateUserView.as_view()),
    path('account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('survey/create/', view=CreateSurveyView.as_view()),
    path('survey/', view=ReadSurveyView.as_view()),
    path('survey/<int:pk>/', view=SurveyGetView.as_view()),
    path('survey/<int:survey_id>/submit-answers/',
         AnswerSubmissionView.as_view(), name='submit-answers'),
    path('survey/get-all/', view=GetAllSurveyByOwnerView.as_view()),
    path('surveys/<int:survey_id>/analysis/', AddUpdateSurveyAnalysis.as_view(), name='update-survey-analysis'),
]
