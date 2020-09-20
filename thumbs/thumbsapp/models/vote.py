from django.db import models
from .idea import Idea
from django.contrib.auth.models import User

class Vote(models.Model):

    '''This is the model for a vote'''

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    idea = models.ForeignKey(Idea, on_delete=models.DO_NOTHING)
    voteDirection = models.IntegerField()

    class Meta:
        verbose_name = ('Vote')
        verbose_name_plural = ('Votes')