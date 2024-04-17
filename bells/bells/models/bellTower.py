from django.db import models
import temple

class bellTower (models.Model,temple):
    id= models.Index()

    Name=models.TextField(max_length=200,null=False)
    TempleId=models.ForeignKey(temple,on_delete=models.CASCADE)