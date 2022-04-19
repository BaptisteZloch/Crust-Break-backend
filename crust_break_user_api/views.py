from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# Create your views here.
@csrf_exempt
def addUser(request): # ok et fonctionne
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    birthdate = request.POST.get('birthdate')
    email = request.POST.get('email')
    password = request.POST.get('password')
    gouts = request.POST.get('gouts')
    User.objects.create(prenom=firstname,nom=lastname,naissance=birthdate,email=email,password=password,gouts=gouts)
    return JsonResponse({'message':'User successfully created !'})

def listUser(request): # ok et fonctionne
    users = [model_to_dict(user) for user in User.objects.all()]
    return JsonResponse({'users':users})
    
def detailUser(request,user_id): # ok et fonctionne
    user_dict = model_to_dict(User.objects.get(pk=user_id))
    user_dict['favorites recipes']=[model_to_dict(recette) for recette in FavoriteReceipe.objects.all().filter(user=User.objects.get(pk=int(user_id)))]
    return JsonResponse(user_dict)

@csrf_exempt
def updateUser(request,user_id): # ok et fonctionne
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    birthdate = request.POST.get('birthdate')
    email = request.POST.get('email')
    password = request.POST.get('password')
    gouts = request.POST.get('gouts')
    user = User.objects.get(pk=user_id)
    user.prenom=firstname
    user.nom=lastname
    user.naissance=birthdate
    user.email=email
    user.password=password
    user.gouts=gouts
    user.save()
    user_dict={'message':'User successfully updated !'}
    user_dict['updated user']=model_to_dict(user)
    return JsonResponse(user_dict)


def deleteUser(request): # ok et fonctionne
    user_id = request.GET.get('user_id')
    user = User.objects.get(pk=int(user_id))
    user.delete()
    return JsonResponse({'message':'User successfully removed !'})

@csrf_exempt
def addRecetteToDo(request, user_id):
    recette_id = request.GET['recette_id']
    recette_name = request.GET['recette_name']
    meal_date = request.GET['meal_date']
    user_id = user_id
    recette_todo = ToDoReceipe(recette_id,recette_name,meal_date,user_id)
    recette_todo.save()
    return JsonResponse({'message':'ok, recette ajoutée !'})
    #  si il n'y a pas de classe Recettes tout court chercher dans toute l'api
    
@csrf_exempt
def addRecetteFavorites(request, user_id): # ok et fonctionne
    recette_id = int(request.POST.get('recette_id'))
    recette_name = str(request.POST.get('recette_name'))
    user = User.objects.get(pk=int(user_id))

    recette_favorite = FavoriteReceipe.objects.create(receipe_id=recette_id,receipe_name=recette_name,user=user)
    recette_favorite.save()
    return JsonResponse({'message':'Recipe added to favorites !'})
    
def deleteRecetteToDo(request,user_id):
  recette_id = request.GET['recette_id']
  user_id = user_id
  recette_todo = ToDoReceipe(recette_id,recette_name,meal_date,user_id)
  recette_todo.delete()
  return JsonResponse({'message':'ok, recette supprimée !'})

@csrf_exempt
def deleteRecetteFavorites(request,user_id): # ok et fonctionne
    recette_id = request.GET.get('recette_id')
    user = User.objects.get(pk=int(user_id))
    recette_favorite = FavoriteReceipe.objects.get(receipe_id=recette_id,user=user)
    recette_favorite.delete()
    return JsonResponse({'message':'Recipe removed from favorites ! '})
  

def getRecetteToDo(request, user_id):
    recettes = [model_to_dict(recette) for recette in ToDoReceipe.objects.all().filter(user=User.objects.get(pk=int(user_id)))]
    return JsonResponse({'recipes':recettes})
    
def getRecetteFavorites(request, user_id): # ok et fonctionne
    recettes = [model_to_dict(recette) for recette in FavoriteReceipe.objects.all().filter(user=User.objects.get(pk=int(user_id)))]
    return JsonResponse({'recipes':recettes})

def getRecettesRecommadations(request,user_id):
    return
