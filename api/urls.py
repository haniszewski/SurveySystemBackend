from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt import views as jwt_views

from .views import hello_world, CreateAccountView, CreateSurveyView, ReadSurveyView, GetAllSurveyByOwnerView

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
    path('account/create', view=CreateAccountView.as_view()),
    path('account/login', view=jwt_views.TokenObtainPairView.as_view()),
    path('survey/create', view=CreateSurveyView.as_view()),
    path('survey/', view=ReadSurveyView.as_view()),
    path('survey/get-all', view=GetAllSurveyByOwnerView.as_view()),
]
