import os
import pandas as pd


# Dictionary of pairs (currency, coefficient), used to convert the different 
# currencies in the USA budget data to dollars. Example: EUR 5 => $ (1.19 * 5)
DICT_CURRENCY = {'GBP': 1.39, 'CAD': 0.79, 'PYG': 0.00015, 'ESP': 1.19,
 'AUD': 0.77, 'EUR': 1.19, 'RUR': 0.014, '$': 1}
  
# Convert [currency] amount to [dollar] amount
def convert_amount_to_dollar(currency, amount):
    if currency in DICT_CURRENCY.keys():
        return amount*DICT_CURRENCY[currency]
    # Error: currency is not in DICT_CURRENCY, just return amount
    else:
        return amount

def convert_budget_to_amount(budget):
    amount = budget.split(' ')
    return convert_amount_to_dollar(amount[0], int(amount[1]))

def handle_queries():
    dirname = os.path.split(os.path.abspath(__file__))[0] + '/files/movies.csv'
    df = pd.read_csv(dirname, low_memory=False)
    df = df[df['country'] == 'USA']['budget']
    df = df.fillna('$ 0')
    count_movies = df.count()
    total_cost = df.apply(convert_budget_to_amount).sum()
    avg_cost = total_cost/count_movies
    return (int(avg_cost), int(total_cost))
