# API rest with django rest framework

## Install

```
$ pipenv install --dev
$ pipenv shell
$ cd /myproject
$ python manage.py runserver
```

## API end points
```
$ python
$ import requests
$ url = 'http://127.0.0.1:8000/
```

# GET
```
$ r = requests.get(url)
$ r.text
```

# POST
```
$ r = requests.post(url, files={'file': open('your_file.txt', 'rb')})
$ r.text

you have to post movies.csv file in order to make the queries
```
# PUT
```
$ r = requests.put(url, data={'query': YOUR_QUERY})
$ r.text

YOUR_QUERY can be: 'total', 'average'
