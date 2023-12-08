from rest_framework import serializers
from django.contrib.auth.models import User
from controllers.models import *
from .schemas import *

class FormInputSerializerToJson(serializers.ModelSerializer):
    class Meta:
        model = FormInput
        fields = ['pk','survey', 'type', 'order', 'text', 'details', 'placeholder']


class FormInputChoiceSerializerToJson(serializers.ModelSerializer):
    class Meta:
        model = FormInputChoice
        fields = ['pk','order', 'input', 'text']

class AnalysisSchemaSerializer(serializers.Serializer):
    analysis_schema = serializers.JSONField()

    def validate_analysis_schema(self, value):
        schema = RootAnalysisSchema()
        errors = schema.validate(value)
        if errors:
            raise serializers.ValidationError(errors)
        return value