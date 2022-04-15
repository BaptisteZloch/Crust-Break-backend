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
        param_string = {
            "query":query_dict['name'],#name of the food : burger, pizza...
            "cuisine":query_dict['cuisine'],#name of the cuisine : american, african...
            "type":query_dict['type'],#type of meal : main course, entry...
            "diet":query_dict['diet'],#type of diet : paleo, primal, and vegetarian...
            "excludeIngredients":query_dict['exclude'],# exemple : coconut, mango
            "instructionsRequired":True,
            "number":20,
            }
        url ='https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/searchComplex'

        response = requests.get(url=url,headers=headers,params=param_string)
        response_content_dict = json.loads(response.content.decode("utf-8"))
        return dict(response_content_dict)

    def getTextFromImage(self, image_file_name):
        image_url = f'http://94.247.183.221:8020/static/uploaded_receipts/{image_file_name}'

        url = "https://ocrly-image-to-text.p.rapidapi.com/"

        #querystring = {"imageurl":image_url,"filename":"sample.jpg"}

        headers = {
            "X-RapidAPI-Host": "ocrly-image-to-text.p.rapidapi.com",
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY
        }

        #response = requests.get(url=url,headers=headers,params=querystring)
        #response_content_str = str(response.content.decode("utf-8"))
        #return response_content_str

    def getIngredientsFromText(self, raw_text):
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/detect"

        payload = f'text={raw_text}'
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY
        }

        response = requests.post(url, data=payload, headers=headers)
        response_content_dict = json.loads(response.content.decode("utf-8"))
        ingredient_list = []
        for ingredient in response_content_dict['annotations']:
            if ingredient['tag'] == 'ingredient':
                ingredient_list.append(ingredient['annotation'])
        return ','.join(ingredient_list)

    def searchRecipeByIngredient(self, ingredients):
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
        querystring = {"ingredients":ingredients,"number":"10","ignorePantry":"true","ranking":"1"}

        headers = {
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY
        }

        response = requests.get(url, headers=headers, params=querystring)
        response_content_dict = json.loads(response.content.decode("utf-8"))
        return {"results": response_content_dict}
    
    def getIngredients(self, recette_id):
        headers = {
            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            "X-RapidAPI-Key": settings.RAPIDAPI_KEY
        }
        url =f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recette_id}/information'
        response = requests.get(url=url,headers=headers)
        response_content_dict = dict(json.loads(response.content.decode("utf-8")))
        ingredients_reciept = []
        for ingredient in response_content_dict['extendedIngredients']:
            ingredient_dict = {}
            ingredient_dict['quantity'] = "{} {}".format(ingredient['measures']["metric"]['amount'],ingredient['measures']["metric"]['unitShort'])
            ingredient_dict['ingredient'] = ingredient['name']
            ingredients_reciept.append(ingredient_dict)

        return {'list':ingredients_reciept}