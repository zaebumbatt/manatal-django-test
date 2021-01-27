# manatal-django-test

# How to use:
1. Go to browsable API:
 - http://school-api.ml/api/
2. Create user and then log in:
 - http://school-api.ml/api/register/
   
   Required fields: username, email, password.


 - http://school-api.ml/api/login/
3. List/create/update/delete students or school:
 - http://school-api.ml/api/students/
      
   Required fields: first_name, last_name, school.
   

 - http://school-api.ml/api/schools/
   
   Required fields: name, school_type, max_students.
4. Check all logs(need to log in as admin):
   - ```username: admin```
   - ```password: admin4321```
   
   All logs: 
   - http://school-api.ml/api/logs/
   
   Logs for User model:
   - http://school-api.ml/api/logs/users/

   Logs for Student model:
   - http://school-api.ml/api/logs/students/

   Logs for School model:
   - http://school-api.ml/api/logs/schools/
   
   Logs with api calls initiated by specific user:
   - http://school-api.ml/api/logs/?username= ```username```
   
   *Put username after an equal sign.*
   
   Logs with a specific object mentioned:
   - http://school-api.ml/api/logs/?obj= ```obj```

   *Instead of "obj" you can use: first_name, last_name, school_name, school_type.*

# Run on you local machine
1. Clone repository https://github.com/zaebumbatt/manatal-django-test.git
2. Open manatal-django-test folder, create and activate virtual enviroment, install requirements, create .env file:
   
    - ```cd manatal-django-test```
   
    - ```python3 -m venv venv```
   
    - ```. venv/bin/activate```
   
    - ```python -m pip install -r requirements.txt```
   
    - ```touch .env```
3. Fill .env with this data:
   - DB_ENGINE=django.db.backends.postgresql_psycopg2
   - DB_NAME=```your postgresql db name```
   - POSTGRES_USER=```your postgresql db username```
   - POSTGRES_PASSWORD=```your postgresql db password```
   - DB_HOST=```your postgresql db host```
   - DB_PORT=```your postgresql db port```
   - SECRET_KEY=```your django secret_key```
   - MC=```mongodb+srv://...```
   - MC_USERNAME=```your mongodb username```
   - MC_PASSWORD=```your mongodb password```
4. Add migrations and runserver:
   
   - ```python manage.py makemigrations```
   
   - ``` python manage.py migrate```
     
   - ``` python manage.py migrate --database=remote```
     
   - ```python manage.py runserver```