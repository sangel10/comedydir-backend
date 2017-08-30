from django.db import models

# Create your models here.

class BasicEvent(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date = models.DateTimeField('event date')


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
