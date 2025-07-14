from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    source = models.CharField(max_length=200)
    tags = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title
