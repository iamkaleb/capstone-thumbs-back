from django.db import models
from .idea import Idea

class IdeaImage(models.Model):

    '''This is the model for an idea image'''

    idea = models.ForeignKey(Idea, on_delete=models.DO_NOTHING)
    url = models.URLField()

    class Meta:
        verbose_name = ('Idea_Image')
        verbose_name_plural = ('Idea_Images')

    def __str__(self):
        return self.url