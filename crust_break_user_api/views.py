from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *


# Create your views here.


# Create your views here.
def addUser(request):
    return
def listUser(request):
    
    return
def detailUser(request):
    return
def updateUser(request):
    return
def deleteUser(request):
    return


def addRecetteToDo(request, user_id):
    recette_id = request.GET['recette_id']
    recette_name = request.GET['recette_name']
    meal_date = request.GET['meal_date']
    user_id = user_id
    recette_todo = ToDoReceipe(recette_id,recette_name,meal_date,user_id)
    recette_todo.save()
    return JsonResponse({'message':'ok, recette ajoutée !'})
    #  si il n'y a pas de classe Recettes tout court chercher dans toute l'api
    
    
def addRecetteFavorites(request, user_id):
  recette_id = request.GET['recette_id']
  recette_name = request.GET['recette_name']
  user_id = user_id
  recette_favorite = FavoriteReceipe(recette_id,recette_name,user_id)
  recette_favorite.save()
  return JsonResponse({'message':'La recette a bien été ajoutée aux favoris'})


def deleteRecetteToDo(request,user_id):
  recette_id = request.GET['recette_id']
  recette_name = request.GET['recette_name']
  meal_date = request.GET['meal_date']
  user_id = user_id
  recette_todo = ToDoReceipe(recette_id,recette_name,meal_date,user_id)
  recette_todo.delete()
  return JsonResponse({'message':'ok, recette supprimée !'})


def deleteRecetteFavorites(request,user_id):
    recette_id = request.GET['recette_id']
    recette_name = request.GET['recette_name']
    user_id = user_id
    recette_favorite = FavoriteReceipe(recette_id, recette_name,user_id)
    recette_favorite.delete()
    return JsonResponse({'message':'La recette a bien été supprimée des favoris'})
  

def getRecetteToDo(request, user_id):
    #request.GET['recette_id'] #POST
    recette_id=request.GET.get('recette_id') #GET
    recette_todo = ToDoReceipe.objects.get(receipe_id=recette_id)
    return JsonResponse(recette_todo)

    

def getRecetteFavorites(request, user_id):
    recette_id=request.GET.get('recette_id')
    recette_favorite = FavoriteReceipe.objects.get(receipe_id=recette_id)
    return JsonResponse(recette_favorite)

def getRecettesRecommadations(request,user_id):
    return
