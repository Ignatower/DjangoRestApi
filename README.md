# API rest with django rest framework

## Install

```
This project uses postgreSQL (https://www.postgresql.org/)
you need to install it and create a DB with the next properties:

NAME: MOVIESDB

USER: postgres

PASSWORD': postgres

HOST: localhost

PORT: 5432

Then run:

$ pipenv install --dev
$ pipenv shell
$ cd /myproject
$ python manage.py runserver
```

## API end points
```
$ python
$ import requests
$ url = 'http://127.0.0.1:8000/'
```

# GET
```
$ r = requests.get(url)
$ r.text

or

$ r = requests.get(url+YOUR_QUERY)
$ r.text

YOUR_QUERY can be: 'total/', 'average/'

you have to post movies.csv file in order to make that queries
```

# POST
```
$ r = requests.post(url, files={'file': open('your_file.txt', 'rb')})
$ r.text
```