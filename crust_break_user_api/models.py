from django.db import models


# Create your models here.
class User(models.Model):
    prenom = models.CharField(max_length=250)
    nom = models.CharField(max_length=250)
    naissance = models.DateField()
    email = models.EmailField()
    password = models.CharField(max_length=250)
    gouts = models.JSONField()
    def __str__(self):
        return f'{self.prenom} {self.nom}'
class ToDoReceipe(models.Model):

    MEAL_TYPES = (('breakfast','breakfast'),('lunch','lunch'),('dinner','dinner'))
    receipe_id = models.PositiveIntegerField()
    receipe_name = models.CharField(max_length=250)
    meal_date = models.DateField()
    meal_type = models.CharField(max_length=200,choices=MEAL_TYPES,null=True)
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



    