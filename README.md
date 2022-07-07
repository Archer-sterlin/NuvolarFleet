# Django Project! 

Information about the application. 
Input the following commands in the terminal after creating and activating venv in project directory 
pipenv can also be used for venv

1. `pip install -r requirements.txt` or `pipenv install` if you are using pipenv 
2. Create a `.env` File and add the following `SECRET_KEY=yoursecret` and in the next line `DEBUG=True` if you want debugging
3. run `python manage.py test` run test
4. run `python manage.py runserver` to start local server
5. while the server is running, make a request to `http://127.0.0.1:8000/swagger/` for openapi documentation 
6. time range request parameter format  `day-month-year-hours:minutes:seconds` i.e `08-07-2022+02:50:00` 
