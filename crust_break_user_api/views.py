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
    recette_id = int(request.POST.get('recette_id'))
    recette_name = str(request.POST.get('recette_name'))
    meal_date = request.POST.get('meal_date')
    meal_type = str(request.POST.get('meal_type'))
    user = User.objects.get(pk=int(user_id))
    recette_favorite = ToDoReceipe.objects.create(receipe_id=recette_id,
                                                        receipe_name=recette_name,
                                                        meal_date=meal_date,
                                                        meal_type=meal_type,
                                                        user=user)
    
    recette_favorite.save()
    return JsonResponse({'message':'Recipe added to the todo list !'})
    
@csrf_exempt
def addRecetteFavorites(request, user_id): # ok et fonctionne
    recette_id = int(request.POST.get('recette_id'))
    recette_name = str(request.POST.get('recette_name'))
    user = User.objects.get(pk=int(user_id))

    recette_favorite = FavoriteReceipe.objects.create(receipe_id=recette_id,receipe_name=recette_name,user=user)
    recette_favorite.save()
    return JsonResponse({'message':'Recipe added to favorites !'})
    
def deleteRecetteToDo(request,user_id):
    recette_id = request.GET.get('recette_id')
    meal_date = request.GET.get('meal_date')
    meal_type = str(request.GET.get('meal_type'))
    user = User.objects.get(pk=int(user_id))
    ToDoReceipe.objects.get(receipe_id=recette_id,meal_date=meal_date,
                                            meal_type=meal_type,user=user).delete()
    recettes = [model_to_dict(recette) for recette in ToDoReceipe.objects.all().filter(user=User.objects.get(pk=int(user_id)))]
    return JsonResponse({'message':'Recipe removed from todo ! ','todo recipes':recettes})

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

@csrf_exempt
def checkUserCanSignUp(request):
    if User.objects.filter(email=str(request.POST.get('email'))).exists():
        return JsonResponse({'code':-1,'message':'Error ! Email already exists...'})
    elif User.objects.filter(password=str(request.POST.get('password'))).exists():
        return JsonResponse({'code':-1,'message':'Error ! Password already exists...'})
    else:
        return JsonResponse({'code':1,'message':'Success ! User can signup'})

@csrf_exempt
def checkUserCanSignIn(request):
    if User.objects.filter(email=str(request.POST.get('email'))).exists() and User.objects.filter(password=str(request.POST.get('password'))).exists():
        return JsonResponse({'code':1,'message':'Success ! User can signup','user':model_to_dict(User.objects.filter(password=str(request.POST.get('password')),email=str(request.POST.get('email')))[0])})
    else:
        return JsonResponse({'code':-1,'message':'Error ! Credentials invalid...'})

def getRecettesRecommadations(request,user_id):
    return
