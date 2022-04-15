import re
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
    query = Api().objects.all().get(id=receipe_id)
    return JsonResponse(FavoritesReceipe.add(query))


def deleteRecetteToDo(request,user_id):
    return


def deleteRecetteFavorites(request,user_id):
    return

def getRecetteToDo(request, user_id):
    #request.GET['recette_id'] #POST
    recette_id=request.GET.get('recette_id') #GET
    recette_todo = ToDoReceipe.objects.get(receipe_id=recette_id)
    return JsonResponse(recette_todo)

def deleteRecetteFavorites(request):
    return
    
def getRecetteFavorites(request, user_id):
    return(RecettesFavorites().getRecipeInformations(receipe_id))

def deleteRecetteFavorites(request):
    return


def getRecetteFavorites(request, user_id):
    return(RecettesFavorites().getReceipeInformations(receipe_id))



def getRecettesRecommadations(request,user_id):
    return
# def generateListeCourses(request):
#     return
# def generateReceipe(request):
#     return