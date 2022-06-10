import codecs
import re
import uuid
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .api import *
import base64
from base64 import decodestring
import os
from django.contrib.staticfiles.storage import staticfiles_storage

def detailRecette(request,recette_id):
    return JsonResponse(Api().getRecipeInformations(recette_id))

def generateListeCourses(request):
    if request.GET.get('recipe') is not None or request.GET.get('recipe') is not '' :
        return JsonResponse(Api().getIngredients(int(request.GET.get('recipe'))))
    else:
        return JsonResponse({'error':{'message':'missing the recipe id to search a recipe...'}})
    

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


def generateRecipe(request):
    data = bytes(request.GET.get('imageB64'),'utf8')
    file_name =str(uuid.uuid4())+ ".jpeg"
    with open(staticfiles_storage.path('uploaded_receipts/'+file_name), "wb") as fh:
        fh.write(base64.decodebytes(data))
        #fh.write(codecs.decode(strOne.strip(),'base64'))  
        
    text_in_image = "I like to eat delicious tacos. Only cheeseburger with cheddar are better than that. But then again, pizza with pepperoni, mushrooms, and tomatoes is so good!"#Api().getTextFromImage(file_name)
    ingredient_in_text= Api().getIngredientsFromText(text_in_image)

    return JsonResponse(Api().searchRecipeByIngredient(ingredient_in_text))