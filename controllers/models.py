from django.db import models
from django.contrib.auth.models import AbstractUser

class SystemUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    
class SurveyStatus(models.Model):
    name = models.CharField(max_length=255)

class Survey(models.Model):
    name = models.CharField(max_length=255, help_text="Enter the name of the survey")
    # status = models.FloatField(SurveyStatus, on_delete=models.PROTECT)
    start_date = models.DateField(help_text="Enter the start date of the survey")
    end_date = models.DateField(help_text="Enter the end date of the survey")
    salt = models.CharField(max_length=255, help_text="abc",default="abc")
    
    
class SurveyPermissions(models.Model):
    name = models.CharField(max_length=255, help_text="Enter the name of the survey")
    
class SurveyOwners(models.Model):
    user = models.ForeignKey(SystemUser, on_delete=models.PROTECT)
    survey = models.ForeignKey(Survey,on_delete=models.PROTECT)
    permissions = models.ForeignKey(SurveyPermissions,on_delete=models.PROTECT)
    
class SurveyParticipants(models.Model):
    survey = models.ForeignKey(Survey,on_delete=models.PROTECT)
    email_crypt = models.CharField(max_length=255, help_text="")


class InputType(models.Model):
    name = models.CharField(max_length=255, help_text="Enter the type of question (e.g. Multiple Choice, Text, Rating)")

class FormInput(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='forms')
    type = models.ForeignKey(InputType, on_delete=models.CASCADE, related_name='forms')
    order = models.IntegerField()
    text = models.TextField(help_text="Enter the text for the question")


class FormInputChoice(models.Model):
    order = models.IntegerField(null=False)
    input = models.ForeignKey(FormInput, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255, help_text="Enter the text for this choice",null=True)
    

class SurveyParticipantAnswer(models.Model):
    choice = models.ForeignKey(FormInputChoice, on_delete=models.CASCADE, related_name='answerscheckbox', null=True)
    value_float = models.FloatField(null=True)
    value_int = models.IntegerField(null=True)
    value_text = models.TextField(null=True)
    participant = models.ForeignKey(SurveyParticipants, on_delete=models.PROTECT, null=True)
    
