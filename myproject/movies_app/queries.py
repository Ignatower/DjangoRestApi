import os
import csv


# Dictionary of pairs (currency, coefficient), used to convert the different 
# currencies in the USA budget data to dollars. Example: EUR 5 => $ (1.19 * 5)
dict_currency = {'GBP': 1.39, 'CAD': 0.79, 'PYG': 0.00015, 'ESP': 1.19,
 'AUD': 0.77, 'EUR': 1.19, 'RUR': 0.014}
  

# Convert [currency] amount to [dollar] amount
def convert_amount_to_dollar(currency, amount):
    if currency in dict_currency.keys():
        return amount*dict_currency[currency]
    # Error: currency is not in dict_currency, just return amount
    else:
        return amount

# Return the queries of exercise 2. 
def handle_queries():
    """
        Return (avg_cost, total_cost), where:
            avg_cost is: costo promedio por pelicula de todas las peliculas cuyo pais es USA
            total_cost is: costo total (budget) de todas las peliculas cuyo pais es USA 
    """
    count_movies_USA, total_cost = 0, 0
    dirname = os.path.split(os.path.abspath(__file__))[0] + '/files/movies.csv'
    with open(dirname, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['country'] == 'USA':
                count_movies_USA += 1
                if row['budget']:
                    budget = row['budget'].split(' ')
                    if budget[0] != '$':
                        total_cost += convert_amount_to_dollar(budget[0], int(budget[1]))
                    else:
                        total_cost += int(budget[1])

    avg_cost = total_cost/count_movies_USA

    return (int(avg_cost), int(total_cost))