from django.db import models
from .group import Group
from django.contrib.auth.models import User

class Poll(models.Model):

    '''This is the model for a poll'''

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name = ('Poll')
        verbose_name_plural = ('Polls')

    def __str__(self):
        return self.title