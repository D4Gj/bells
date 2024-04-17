from django.db import models
import bell
import bellTower

class queryForMovement (models.Model,bellTower,bell):
    id= models.Index()

    Date=models.DateField()
    Status=models.TextChoices()
    BellTowerId=models.ForeignKey(bellTower,on_delete=models.CASCADE)
    BellId=models.ForeignKey(bell,on_delete=models.CASCADE)