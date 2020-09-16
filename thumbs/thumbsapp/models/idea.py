from django.db import models
from .poll import Poll
from django.contrib.auth.models import User

class Idea(models.Model):

    '''This is the model for an idea'''

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    poll = models.ForeignKey(Poll, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name = ('Idea')
        verbose_name_plural = ('Ideas')

    def __str__(self):
        return self.title