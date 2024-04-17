from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class user (models.Model,Importable):
    id= models.Index()

    Name=models.TextField(max_length=200)
    Role=models.TextField(max_length=60)
    PhoneNumber=PhoneNumberField(region="RU")
    Email=models.EmailField()
