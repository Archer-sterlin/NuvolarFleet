# Nuvolar Feet Manager Project Built with Django and Django rest-framework

Information about the application. 
Input the following commands in the terminal after creating and activating venv in project directory 
pipenv can also be used for venv

1. `pip install -r requirements.txt` or `pipenv install` if you are using pipenv 
2. Create a `.env` File and add the following `SECRET_KEY=yoursecret`, in the next line `DEBUG=True` if you want debugging.
3. run `python manage.py test` run test
4. run `python manage.py runserver` to start local server
5. while the server is running, make a request to `http://0.0.0.0:8000/swagger/` for openapi documentation 
6. time range request parameter format  `day-month-year-hours:minutes:seconds` i.e `08-07-2022+02:50:00` 



## Django browesable API

### run `python manage.py runserver` to start local server
## endpoints:

# aircraft CRUD operations
`http://0.0.0.0:8000/api/v1/aircrafts/`
`http://0.0.0.0:8000/api/v1/aircrafts/<uuid:pk>/`

# airport CRUD operations
`http://0.0.0.0:8000/api/v1/airport/`
`http://0.0.0.0:8000/api/v1/<icao>/`

# flight CRUD operations
`http://0.0.0.0:8000/api/v1/flight/`
`http://0.0.0.0:8000/api/v1/flight/edit/<uuid:pk>/`
`http://0.0.0.0:8000/api/v1/flights/departure/time/range/<from>/<to>/`
`http://0.0.0.0:8000/api/v1/flights/departure/<icao>/`
`http://0.0.0.0:8000/api/v1/flights/arrival/<icao>/`
    
 

## Runing Docker


#### Make sure you have docker installed on you local machine or 
download (mac with intel chip) https://www.docker.com/products/docker-desktop/
#### Drag and drop into application folder to installed
#### Run the docker app 
#### docker uses postgres for database. To configure database settings, set `DOCKER=True`  in settings.py on  `it should be in line 32`
#### to start server in the container, run  `docker-compose up` in a terminal window opened in the same directory as docker-compose.yml file
#### to stop server in the container, push `control + c` run `docker-compose down` in a terminal window opened in the same directory as docker-compose.yml file
#### while docker-compose is down or up, you can run normal commands like migrate, makemigrations, createsuperuser etc like so in another terminal window
`docker-compose run  web  python manage.py createsuperuser`

## endpoints (port for docker 8080 as indicated below):

# aircraft CRUD operations
`http://0.0.0.0:8080/api/v1/aircrafts/`
`http://0.0.0.0:8080/api/v1/aircrafts/<uuid:pk>/`

# airport CRUD operations
`http://0.0.0.0:8080/api/v1/airport/`
`http://0.0.0.0:8080/api/v1/<icao>/`

# flight CRUD operations
`http://0.0.0.0:8080/api/v1/flight/`
`http://0.0.0.0:8080/api/v1/flight/edit/<uuid:pk>/`
`http://0.0.0.0:8080/api/v1/flights/departure/time/range/<from>/<to>/`
`http://0.0.0.0:8080/api/v1/flights/departure/<icao>/`
`http://0.0.0.0:8080/api/v1/flights/arrival/<icao>/`