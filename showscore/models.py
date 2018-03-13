from django.db import models

# Create your models here.
class Score(models.Model):
    id = models.IntegerField(primary_key=True)
    posted = models.IntegerField()
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=30)
