from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):

    '''This is the model for a group'''

    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=250)

    class Meta:
        verbose_name = ('Group')
        verbose_name_plural = ('Groups')

    def __str__(self):
        return self.title

    