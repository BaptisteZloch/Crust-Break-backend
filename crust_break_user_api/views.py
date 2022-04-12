from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

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

def addRecetteToDo(request,id):
        query = RecetteToDo.objects.all().get(id=receipe_id)
        query.add()
        return HttpResponse("Recette Ajoutée")
    

def addRecetteFavorites(request):
    return

def deleteRecetteToDo(request, ID):
    query = RecetteToDo.objects.all().get(ID=receipe_id)
    query.delete()
    return HttpResponse("Recette supprimée")
    return render (request, 'deleteRecetteToDo.html', )
   
def deleteRecetteFavorites(request):
    return
def getRecetteToDo(request,nom):
    RecetteToDo.objects.all().get(nom=receipe_name).add()
    return HttpResponse()

def deleteRecetteFavorites(request):
    return
def getRecetteFavorites(request):
    return
def getRecettesRecommadations(request):
    return
def generateListeCourses(request):
    return
def generateReceipe(request):
    return