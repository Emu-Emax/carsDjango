import requests


def fetch_car_models(car_make):
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/' + car_make + '?format=json'
    r = requests.get(url)
    car_models = r.json()
    return car_models['Results']