from django.db import models
from .idea import Idea

class IdeaVideo(models.Model):

    '''This is the model for an idea video'''

    idea = models.ForeignKey(Idea, on_delete=models.DO_NOTHING)
    url = models.URLField()

    class Meta:
        verbose_name = ('Idea_Video')
        verbose_name_plural = ('Idea_Videos')

    def __str__(self):
        return self.url