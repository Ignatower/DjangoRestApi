from django.db import models


class Query(models.Model):
    title = models.CharField(max_length=100, default='')
    value = models.CharField(max_length=100, default='')


    def __str__(self):
        return self.title


class File(models.Model):
    file = models.FileField(upload_to='movies_app/files')


class Movie(models.Model):
    imdb_title_id = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    original_title = models.CharField(max_length=250)
    # ----------- DATE  -----------------
    year = models.IntegerField()
    date_published = models.DateField()
    # ------------------------------------------------
    genre = models.CharField(max_length=100)
    duration = models.FloatField()
    country = models.CharField(max_length=250)
    language = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    production_company = models.CharField(max_length=200)
    actors = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    avg_vote = models.FloatField()
    votes = models.FloatField()
    # ---------- MONEY ---------
    budget = models.FloatField()
    usa_gross_income = models.FloatField()
    worlwide_gross_income = models.FloatField()
    # ------------------------------------------------
    metascore = models.FloatField()
    reviews_from_users = models.FloatField()
    reviews_from_critics = models.FloatField()
    # ----------- CURRENCY ------------------------
    budget_currency = models.CharField(max_length=100)
    usa_gross_income_currency = models.CharField(max_length=100)
    worlwide_gross_income_currency = models.CharField(max_length=100)

    def __str__(self):
        return self.title
