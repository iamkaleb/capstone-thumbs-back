from django.db import models
from .group import Group
from django.contrib.auth.models import User

class GroupUser(models.Model):

    '''This the model for a group user'''

    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ('Group_User')
        verbose_name_plural = ('Group_Users')