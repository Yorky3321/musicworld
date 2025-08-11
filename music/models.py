from django.db import models

# Create your models here.
class sound_base(models.Model):
    path = models.CharField(max_length=100)
    notes = models.CharField(max_length=5, unique=True)

