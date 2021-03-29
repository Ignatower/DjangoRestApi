import os
import time
import pandas as pd
import numpy as np
from itertools import islice
from movies_app.models import Movie, Query


DIRNAME = dirname = os.path.split(os.path.abspath(__file__))[0] + '/files/'

FIELDS = ['imdb_title_id', 'title', 'original_title', 'year', 'date_published',
           'genre', 'duration', 'country', 'language', 'director', 'writer',
           'production_company', 'actors', 'description', 'avg_vote', 'votes',
           'budget', 'usa_gross_income', 'worlwide_gross_income', 'metascore',
           'reviews_from_users', 'reviews_from_critics', 'budget_currency',
            'usa_gross_income_currency', 'worlwide_gross_income_currency']

# Dictionary of pairs (currency, coefficient), used to convert the different 
# currencies in the USA budget data to dollars. Example: EUR 5 => $ (1.19 * 5)
DICT_CURRENCY = {'GBP': 1.39, 'CAD': 0.79, 'PYG': 0.00015, 'ESP': 1.19,
 'AUD': 0.77, 'EUR': 1.19, 'RUR': 0.014, '$': 1}

def fix_date(elem):
    if len(elem) == 4:
        return elem + '-08-20'
    elif len(elem) == 13:
        return '2019-08-20'
    else:
        return elem

def fix_date_published(df):
    df['date_published'] = df['date_published'].apply(fix_date)

def fix_year(df):
    df.loc[df['year'] == 'TV Movie 2019', 'year'] = '2019'

def create_cols(df):
    N = len(df['budget'])
    new_empty_col = pd.Series(np.full(N, ''))
    df.insert(len(df.columns), 'budget_currency', new_empty_col)
    df.insert(len(df.columns), 'usa_currency',new_empty_col)
    df.insert(len(df.columns), 'world_currency', new_empty_col)

def get_currency(amount):
    return amount.split(' ')[0]

def get_number(amount):
    return float(amount.split(' ')[1])

def fix_money(df, old_col, new_col):
    df[old_col].fillna('$ 0', inplace=True)
    df[new_col] = df[old_col].apply(get_currency)
    df[old_col] = df[old_col].apply(get_number)   

def fix_all_money(df):
    create_cols(df)
    fix_money(df, 'worlwide_gross_income', 'world_currency')
    fix_money(df, 'usa_gross_income', 'usa_currency')
    fix_money(df, 'budget', 'budget_currency')

def fix_nan_and_none(df):
    columns = df.columns
    for col in columns:
        col_type = df[col].dtypes
        if col_type == 'object':
            df[col].fillna('', inplace=True)
            df.loc[df[col] == 'None', col] = ''
        else:
            df[col].fillna(0, inplace=True)

# normalize df to save it in DB
def normalize_db(df):
    fix_year(df)
    fix_date_published(df)
    fix_all_money(df)
    fix_nan_and_none(df)

def create_movie(row):
    movie = Movie()
    i = 0
    for field_name in FIELDS:
        setattr(movie, field_name, row[i])
        i += 1

    return movie

# save movies objects in DB
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#bulk-create
# https://tech.serhatteker.com/post/2019-09/django-db-bulk-create/
def create_db(movies_list):
    batch_size = 10000
    while True:
        batch = list(islice(movies_list, batch_size))
        if not batch:
            break
        Movie.objects.bulk_create(batch, batch_size)

def create_db_from_file(movies):
    dirname = DIRNAME + movies
    df = pd.read_csv(dirname, low_memory=False)
    start_time = time.time()
    normalize_db(df)
    movies_list = (create_movie(row) for row in df.itertuples(index=False))
    print("Normalize + Create movies_list  --- {} seconds ---".format(time.time() - start_time))
    start_time = time.time()
    create_db(movies_list)
    print("Create DB TIME --- {} seconds ---".format(time.time() - start_time))

def create_queries():
    # if the queries do not exist (i.e. MOVIES file have not been created
    # in the past) then, create total and avg queries
    if not Query.objects.filter(title='total').count():
        movies_USA = Movie.objects.filter(country='USA')
        total = 0
        for movie in movies_USA:
            total += movie.budget * DICT_CURRENCY[movie.budget_currency]
        avg = int(total/movies_USA.count())
        total = int(total)

        #avg, total = handle_queries()
        total = '$ ' + str(total)
        query = Query()
        # create query instance of the total cost of the movies
        query.title= 'total'
        query.value = total
        query.save()
        avg = '$ ' + str(avg)
        query = Query()
        # create query instance of the avg cost of the movies
        query.title = 'average'
        query.value = avg
        query.save()
