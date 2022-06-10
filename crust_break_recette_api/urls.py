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

app_name = 'crust_break_recette_api'
urlpatterns = [
    path('detail/<int:recette_id>', views.detailRecette,name="detail_recette"),
    path('search', views.searchRecette,name="search_recette"),
    path('generate-liste-de-courses', views.generateListeCourses,name="generate_liste_course"),
    path('generate-recipe', views.generateRecipe,name="generate_recipe"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
