import requests
import credentials

class ApiHandler:
    @staticmethod
    def get_recipe(ingredients, api_id, api_key):
        url = f'https://api.edamam.com/search?q={",".join(ingredients)}&app_id={api_id}&app_key={api_key}'
        response = requests.get(url)
        data = response.json()
        return data
