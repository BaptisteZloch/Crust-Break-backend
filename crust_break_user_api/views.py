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
    recette_id = request.GET.get('recette_id')
    query = ToDoReceipe.objects.all().get(id=recette_id)
    return JsonResponse(RecetteToDo.add(query))
    #  si il n'y a pas de classe Recettes tout court chercher dans toute l'api
    
    
def addRecetteFavorites(request, user_id):
    query = Api().objects.all().get(id=receipe_id)
    return JsonResponse(FavoritesReceipe.add(query))


def deleteRecetteToDo(request):
    return


def deleteRecetteFavorites(request):
    return

def getRecetteToDo(request, receipe_id):
    return JsonResponse(RecetteToDo().getReceipeInformations(receipe_id))

def deleteRecetteFavorites(request):
    return
    
def getRecetteFavorites(request, receipe_id):
    return(RecettesFavorites().getRecipeInformations(receipe_id))

def deleteRecetteFavorites(request):
    return


def getRecetteFavorites(request, receipe_id):
    return(RecettesFavorites().getReceipeInformations(receipe_id))



def getRecettesRecommadations(request):
    return
# def generateListeCourses(request):
#     return
# def generateReceipe(request):
#     return