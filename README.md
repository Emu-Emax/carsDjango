#Cars Django

Django app which allows you to search in [external API]("https://vpic.nhtsa.dot.gov/api") for car make and model, updating database with cars, voting for them and 
viewing by popularity

####App demo (deployed on Heroku):
    
[App demo](https://cars-api-karol.herokuapp.com/)

####Installation:

1. Build docker image

    sudo docker-compose build

2. Run migrations for first time

    sudo docker-compose run web python3 manage.py migrate

3. Run application

    sudo docker-compose up

####Running tests:
    
    sudo docker-compose run web python3 manage.py test
