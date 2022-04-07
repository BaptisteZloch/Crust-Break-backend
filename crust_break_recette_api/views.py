from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .api import *
import json

def detailRecette(request,recette_id):
    return JsonResponse(Api().getRecipeInformations(recette_id))

def searchRecette(request):
    return