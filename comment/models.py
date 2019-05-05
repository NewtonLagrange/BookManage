from django.db import models
from tinymce.models import HTMLField
from Book.models import User


# Create your models here.
class Comment(models.Model):
    content = HTMLField()
    user = models.ForeignKey(to=User, on_delete=None)

    def __str__(self):
        return self.content
