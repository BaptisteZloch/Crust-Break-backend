import json
import requests
from django.conf import settings

class Api():
    def getRecipeInformations(self, recipe_id):
        headers = {
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY
        }
        url =f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/information'
        

        response = requests.get(url=url,headers=headers)
        response_content_dict = dict(json.loads(response.content.decode("utf-8")))
        url_equipement =f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/equipmentWidget.json'

        response_equi = requests.get(url=url_equipement,headers=headers)
        response_content_dict['equipment'] = dict(json.loads(response_equi.content.decode("utf-8")))['equipment']

        return response_content_dict

    def searchRecipe(self, query_dict):
        headers = {
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY
        }
        url ='https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/searchComplex'

        response = requests.get(url=url,headers=headers)
        response_content_dict = json.loads(response.content.decode("utf-8"))
        return dict(response_content_dict)