from django.db import models
import bellTower

class bell (models.Model,bellTower):
    id= models.Index()

    Name=models.TextField(max_length=200)
    Weight=models.IntegerField(max_length=100)
    Firm=models.IntegerField(max_length=100)
    Audio=models.FileField()
    Status=models.TextChoices()
    Picture=models.FileField()
    BellTowerId=models.ForeignKey(bellTower,on_delete=models.CASCADE)