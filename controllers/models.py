from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    name = models.CharField(max_length=255, help_text="Enter the name of the survey")
    start_date = models.DateField(help_text="Enter the start date of the survey")
    end_date = models.DateField(help_text="Enter the end date of the survey")

class SurveyOwners(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    survey = models.ForeignKey(Survey,on_delete=models.PROTECT)
    permission = models.IntegerField(default=0)


class QuestionType(models.Model):
    name = models.CharField(max_length=255, help_text="Enter the type of question (e.g. Multiple Choice, Text, Rating)")

class Form(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='forms')
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE, related_name='forms')
    order = models.IntegerField()
    question_text = models.TextField(help_text="Enter the text for the question")


class Choice(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255, help_text="Enter the text for this choice")

class AnswerCheckBox(models.Model):
    value = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='answerscheckbox')
