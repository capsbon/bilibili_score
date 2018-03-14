from django.db import models

# Create your models here.
class Score(models.Model):
    bangumi_id = models.IntegerField(primary_key=True)
    score = models.DecimalField(max_digits=2,decimal_places=1,null=True)
    count = models.IntegerField(null=True)
    cover = models.CharField(max_length=127,null=True)
    title = models.CharField(max_length=127,null=True)
    brief = models.CharField(max_length=512,null=True)
    play_count = models.IntegerField(null=True)
    pub_time = models.CharField(max_length=64,null=True)


