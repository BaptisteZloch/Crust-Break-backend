"""epf_projets_site_vitrine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'crust_break_user_api'
urlpatterns = [
    path('add/user', views.AddUser,name="add_user"), #C
    path('list', views.listUser,name="list_user"), #R
    path('detail/<int:user_id>', views.detailUser,name="detail_user"), #R
    path('update/<int:user_id>', views.updateUser,name="update_user"), #U
    path('delete/<int:user_id>', views.deleteUser,name="delete_user"), #D
    
    path('add/to-do/<int:recette_id>', views.AddRecetteToDo,name="add_user_todo_recette"),
    path('<int:user_id>/get/todo-receipes', views.getRecetteToDo,name="get_user_todo_recette"),
    
    path('add/to-favorites/<int:recette_id>', views.AddRecetteToFavorites,name="add_user_favorites_recette"),
    path('<int:user_id>/get/favorites-receipes', views.getRecetteFavorites,name="get_user_todo_recette"),
    #path('search', views.searchRecette,name="search_recette"),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
