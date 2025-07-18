from django.db import models
from django.http import HttpResponse
from flask import Response


class Tag(models.Model):
    tag_string = models.CharField(max_length=15, unique=True)

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, blank=True)



    def __str__(self):
        return self.title

