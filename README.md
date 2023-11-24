# On Windows

### Create venv and activate it
```
py -m venv .venv
./.venv/scripts/activate
```

### Install modules
```
pip install -r requirements.txt
```

## Helpers

### Delete migrations

```
py delete_migrations.py
```

### Make migrations and run

```
py manage.py makemigrations
py manage.py migrate    
```

### Load fixtures

```
py manage.py loaddata input_types permissions survey_status
```

## Run 

```
py manage.py runserver 0.0.0.0:8000
```

# On Linux

On deployment please use gunicorn or other python http server.