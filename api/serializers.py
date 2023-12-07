from rest_framework import serializers
from django.contrib.auth.models import User
from controllers.models import *


class FormInputChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormInputChoice
        fields = ('order', 'text',)


class CreateFormInputSerializer(serializers.ModelSerializer):
    choices = FormInputChoiceSerializer(many=True, required=False)
    details = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    placeholder = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = FormInput
        fields = ('type', 'order', 'text', 'details', 'placeholder', 'choices')

class SurveyPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyPermissions
        fields = ['id', 'name']

class SurveyUserListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    class Meta:
        model = Survey
        fields = ['id', 'name', 'status', 'start_date', 'end_date', 'permissions']
    def get_permissions(self, obj):
        permission = SurveyPermissions.objects.filter(surveyowners__survey=obj).first()
        if permission:
            return SurveyPermissionsSerializer(permission).data
        return None

class FormInputSerializer(serializers.ModelSerializer):
    choices = FormInputChoiceSerializer(many=True, required=False)

    class Meta:
        model = FormInput
        fields = ('type', 'order', 'text', 'choices')
        
class FormInputSingleSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyParticipantAnswer
        fields = ['choice', 'participant']

class FormInputMultiSelectSerializer(serializers.ModelSerializer):
    choice = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=FormInputChoice.objects.all()
    )
    
    def to_internal_value(self, data):
        answer_data = data.get('answer')
        if answer_data is not None:
            data['choice'] = answer_data
            del data['answer']  # Remove 'answer' to avoid unexpected field error

        return super().to_internal_value(data)

    class Meta:
        model = SurveyParticipantAnswer
        fields = ['choice', 'participant']

    def create(self, validated_data):
        choices = validated_data.pop('choice')
        participant = validated_data.get('participant')

        created_ids = []
        for choice in choices:
            survey_participant_answer = SurveyParticipantAnswer.objects.create(
                choice=choice, participant=participant
            )
            created_ids.append(survey_participant_answer.pk)

        return {'created_ids': created_ids}



# Used on validaating new Survey
class SurveyCreateSerializer(serializers.ModelSerializer):
    questions = CreateFormInputSerializer(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'name', 'start_date', 'end_date', 'questions')
        # fields = ('id', 'name', 'start_date', 'end_date', 'questions')


# Used by Participand
class SurveyGetSerializer(serializers.ModelSerializer):
    questions = FormInputSerializer(many=True, source='forms', read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'name', 'questions']


class AnswerSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyParticipantAnswer
        fields = ['choice', 'value_float', 'value_int', 'value_text', 'participant']

    def validate(self, data):
        choice = data.get('answer')
        if choice and not FormInputChoice.objects.filter(form_input=choice.form_input).exists():
            raise serializers.ValidationError(
                "Invalid choice for the question.")
        return data


class CreateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    login = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['login'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['name'],
            last_name=validated_data['surname']
        )
        return user

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        return {
            'email': instance.email,
            'login': instance.username,
            'name': instance.first_name,
            'surname': instance.last_name,
        }
