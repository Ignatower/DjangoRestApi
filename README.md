# API rest with django rest framework

## Install

```
$ pipenv install --dev
$ pipenv shell
$ cd /myproject
$ python manage.py runserver
```

## API end points
# http://127.0.0.1:8000/files/
```
$ python
$ import requests
$ url = http://127.0.0.1:8000/files/
$ r = requests.post(url, files={'file': open('your_file.txt', 'rb')})
$ r.text

you have to post movies.csv file in order to make the queries
```
# http://127.0.0.1:8000/queries/
```
$ python
$ import requests
$ url = http://127.0.0.1:8000/queries/n/
$ r = requests.get(url)
$ r.text

n = 1 query the total cost, n = 2  query the average cost
```