import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class SurveySession(models.Model):
    id = models.AutoField(primary_key=True)

class SystemUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)


class SurveyStatus(models.Model):
    name = models.CharField(max_length=255)

class Survey(models.Model):
    name = models.CharField(
        max_length=255, help_text="Enter the name of the survey")
    status = models.ForeignKey(SurveyStatus, on_delete=models.PROTECT)
    start_date = models.DateField(
        help_text="Enter the start date of the survey")
    end_date = models.DateField(
        help_text="Enter the end date of the survey")
    salt = models.CharField(
        max_length=255, help_text="abc", default="abc", null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    validation_json = models.JSONField(null=True)
    analysis_json = models.JSONField(null=True)
    analysis_result_json = models.JSONField(null=True)
    
    def update_status_by_date(self,d_date):
        if d_date < self.start_date:
            self.status_id = 1
        elif d_date <= self.end_date:
            self.status_id = 3
        else:
            self.status_id = 4
            
        self.save()

class SurveyPermissions(models.Model):
    name = models.CharField(
        max_length=255, help_text="Enter the name of the survey")


class SurveyOwners(models.Model):
    user = models.ForeignKey(SystemUser, on_delete=models.PROTECT)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    permissions = models.ForeignKey(
        SurveyPermissions, on_delete=models.PROTECT)

# class SurveyParticipants(models.Model):
#     survey = models.ForeignKey(Survey,on_delete=models.PROTECT)
#     email_crypt = models.CharField(max_length=255, help_text="")


class InputType(models.Model):
    name = models.CharField(
        max_length=255, help_text="Enter the type of question (e.g. Multiple Choice, Text, Rating)")


class FormInput(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name='forms')
    type = models.ForeignKey(
        InputType, on_delete=models.CASCADE, related_name='forms')
    order = models.IntegerField()
    text = models.TextField(
        help_text="Enter the text for the question", null=True)
    details = models.TextField(
        help_text="Enter the text for the question", null=True)
    placeholder = models.TextField(
        help_text="Enter the text for the question", null=True)


class FormInputChoice(models.Model):
    order = models.IntegerField(null=False)
    input = models.ForeignKey(
        FormInput, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(
        max_length=255, help_text="Enter the text for this choice", null=True)


class SurveyParticipantAnswer(models.Model):
    choice = models.ForeignKey(
        FormInputChoice, on_delete=models.CASCADE, related_name='answerscheckbox', null=True)
    value_float = models.FloatField(null=True)
    value_int = models.IntegerField(null=True)
    value_text = models.TextField(null=True)
    # participant = models.ForeignKey(SurveyParticipants, on_delete=models.PROTECT, null=True)
    participant = models.ForeignKey(SurveySession, on_delete=models.CASCADE)
