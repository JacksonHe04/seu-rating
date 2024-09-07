from django.db import models


class Book(models.Model):
    objects = None
    title = models.CharField(max_length=225)
    author = models.CharField(max_length=225)
    publication_date = models.DateField()

    def __str__(self):
        return self.title

# Create your models here.
