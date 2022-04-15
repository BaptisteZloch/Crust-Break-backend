from django.db import models


# Create your models here.
class User(models.Model):
    prenom = models.CharField(max_length=250)
    nom = models.CharField(max_length=250)
    naissance = models.DateField()
    email = models.EmailField()
    password = models.CharField(max_length=250)
    gouts = models.JSONField()

class ToDoReceipe(models.Model):
    receipe_id = models.PositiveIntegerField()
    receipe_name = models.CharField(max_length=250)
    meal_date = models.DateTimeField()
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name="The related user",
    null=True
    )

    def __str__(self):
        return self.receipe_name
   
class FavoriteReceipe(models.Model):
    receipe_id = models.PositiveIntegerField()
    receipe_name = models.CharField(max_length=250)
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name="The related user",
    null=True
    )
    
    def __str__(self):
        return self.receipe_name



    