# qfxscrape
qfx site scrapper and a facebook chatbot based on it built on django

# introduction
this is just a hobby project to see the possibilies of a facebook chatbot

# instructions

## install the requirements
```pip install -r requirements.txt```

## create local settings
copy and rename the file ```local_settings.sample``` to ```local_settings.py```

## run first time migration
```python manage.py migrate```

## create superuser if you want the access to the admin panel
```python manage.py createsuperuser```

## to fetch shows
```python manage.py fetch_shows```

## to fetch showtimes
```python manage.py fetch_showtimes```

## run the local server
```python manage.py runserver```
