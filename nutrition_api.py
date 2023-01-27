# Description: This file contains the code to make a request to the Nutrition API
import requests

url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"

headers = {
	"X-RapidAPI-Key": "e664c132c9msh0ec92e9381bf2ecp106915jsn1dad27defd00",
	"X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
}

def get_nutrition_info(querystring):
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()
