from django.db import models

#scrapped website

class website(models.Model):
    url = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    html = models.TextField(blank=True)
