from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .api import *
import json

def detailRecette(request,recette_id):
    return JsonResponse(Api().getRecipeInformations(recette_id))

def searchRecette(request):
    if request.GET.get('name') is not None or request.GET.get('name') is not '' :
        query_dict = {
            'name':request.GET.get('name'),#name of the food : burger, pizza...
            'cuisine':request.GET.get('cuisine') if request.GET.get('cuisine') is not None or request.GET.get('cuisine') is not '' else '',#name of the cuisine : american, african...
            'type':request.GET.get('type') if request.GET.get('type') is not None or request.GET.get('type') is not '' else '',#type of meal : main course, entry...
            'diet':request.GET.get('diet') if request.GET.get('diet') is not None or request.GET.get('diet') is not '' else '',#type of diet : paleo, primal, and vegetarian...
            'exclude':request.GET.get('exclude') if request.GET.get('exclude') is not None or request.GET.get('exclude') is not ''  else ''
        }
        return JsonResponse(Api().searchRecipe(query_dict))
    else:
        return JsonResponse({'error':{'message':'missing the query string to search a recipe...'}})