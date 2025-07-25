from django.db import models
from django.http import HttpResponse


class Tag(models.Model):
    tag_string = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.tag_string

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-id']



    def __str__(self):
        return self.title

