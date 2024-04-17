from django.db import models

class temple (models.Model):
    id= models.Index()

    Name=models.TextField(max_length=200)
    Address=models.TextField(max_length=60)