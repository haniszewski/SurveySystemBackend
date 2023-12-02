from rest_framework import serializers
from django.contrib.auth.models import User
from controllers.models import *
from .schemas import *


class AnalysisSchemaSerializer(serializers.Serializer):
    analysis_schema = serializers.JSONField()

    def validate_analysis_schema(self, value):
        schema = RootAnalysisSchema()
        errors = schema.validate(value)
        if errors:
            raise serializers.ValidationError(errors)
        return value