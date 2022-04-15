from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import re
import uuid
from .api import *
import based64 import decodestring
import os
from django.contrib.staticfiles.storage import staticfiles_storage


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





def addRecetteToDo(request, id):
     query = Api().objects.all().get(id=receipe_id)
     return JsonResponse(RecetteToDo.add(query))
    #  si il n'y a pas de classe Recettes tout court chercher dans toute l'api
    
    
def addRecetteFavorites(request, id):
    query = Api().objects.all().get(id=receipe_id)
    return JsonResponse(FavoritesReceipe.add(query))


def deleteRecetteToDo(request):
    return


def deleteRecetteFavorites(request):
    return

def getRecetteToDo(request, receipe_id):
    return JsonResponse(RecetteToDo().getRecipeInformations(receipe_id))

def deleteRecetteFavorites(request):
    return
    
def getRecetteFavorites(request, receipe_id):
    return(RecetteFavorites().getRecipeInformations(receipe_id))



def getRecettesRecommadations(request):
    return
# def generateListeCourses(request):
#     return
# def generateReceipe(request):
#     return