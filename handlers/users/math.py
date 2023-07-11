import requests

from parser.exchange import curs


def math(currency, coin_type, cost_electricity, hash, potreb, komm):
    if coin_type == "Bitcoin":
        url = 'https://whattomine.com/coins/1.json'
        response = requests.get(url)
        json_data = response.json()
        block_reward24 = json_data['block_reward24']
        difficulty = json_data['difficulty']
        exchange_rate_json = json_data['exchange_rate']
        rate = 1e12


    elif coin_type == "Litecoin":
        url = 'https://whattomine.com/coins/4.json'
        response = requests.get(url)
        json_data = response.json()
        block_reward24 = json_data['block_reward24']
        difficulty = json_data['difficulty']
        exchange_rate_json = json_data['exchange_rate_vol'] / 2.538
        rate = 1e9


    elif coin_type == "Ethereum-classic":
        url = 'https://whattomine.com/coins/162.json'
        response = requests.get(url)
        json_data = response.json()
        block_reward24 = json_data['block_reward']
        difficulty = json_data['difficulty']
        exchange_rate_json = json_data['exchange_rate_vol']
        rate = 1e6


    elif coin_type == "Zcash":
        url = 'https://whattomine.com/coins/166.json'
        response = requests.get(url)
        json_data = response.json()
        block_reward24 = json_data['block_reward24']
        difficulty = json_data['difficulty']
        exchange_rate_json = json_data['exchange_rate_vol'] * 2.99
        rate = 1e3


    elif coin_type == "Bitcoin-cash":
        url = 'https://whattomine.com/coins/193.json'
        response = requests.get(url)
        json_data = response.json()
        block_reward24 = json_data['block_reward24']
        difficulty = json_data['difficulty']
        exchange_rate_json = json_data['exchange_rate_vol'] * 2
        rate = 1e12


    else:
        url = 'https://whattomine.com/coins/34.json'
        response = requests.get(url)
        json_data = response.json()
        block_reward24 = json_data['block_reward24']
        difficulty = json_data['difficulty']
        exchange_rate_json = json_data['exchange_rate_vol'] / 7
        rate = 1e9

    currency_now = curs()

    if currency == "RUB ₽":
        exchange_rate = currency_now * float(exchange_rate_json)

    else:
        exchange_rate = float(exchange_rate_json)

    hour = 3600
    day = 3600 * 24
    week = 3600 * 24 * 7
    month = 3600 * 24 * 30

    D = difficulty
    H = rate * float(hash)
    R = block_reward24

    if coin_type == "Bitcoin":
        profit_coin = lambda time: (time * R * H) / (D * pow(2, 32))
        income = lambda incoin: exchange_rate * float(incoin)
        expense = lambda time, exp: float(potreb) / 1000 * time * float(cost_electricity) + (float(exp) *
                                                                                             ((float(komm) / 100)))
        profit = lambda inc, expen: inc - expen
    elif coin_type == "Ethereum-classic":
        profit_coin = lambda time: (time * R * H) / D
        income = lambda incoin: exchange_rate * float(incoin) * 0.93
        expense = lambda time, exp: float(potreb) / 1000 * time * float(cost_electricity) + (float(exp) *
                                                                                             ((float(komm) / 100)))
        profit = lambda inc, expen: inc - expen
    elif coin_type == "Zcash":
        profit_coin = lambda time: (time * R * H) / (D * pow(2, 12.9))
        income = lambda incoin: exchange_rate * float(incoin)
        expense = lambda time, exp: float(potreb) / 1000 * time * float(cost_electricity) + (float(exp) *
                                                                                             ((float(komm) / 100)))
        profit = lambda inc, expen: inc - expen

    elif coin_type == "Bitcoin-cash":
        profit_coin = lambda time: (time * R * H) / (D * pow(2, 32))
        income = lambda incoin: exchange_rate * float(incoin) * 0.55
        expense = lambda time, exp: float(potreb) / 1000 * time * float(cost_electricity) + (float(exp) *
                                                                                             (
                                                                                                 (float(
                                                                                                     komm) / 100))) * 0.8
        profit = lambda inc, expen: inc - expen

    elif coin_type == "Litecoin":
        profit_coin = lambda time: (time * R * H) / (D * pow(2, 32))
        income = lambda incoin: exchange_rate * float(incoin) * 1.1
        expense = lambda time, exp: float(potreb) / 1000 * time * float(cost_electricity) + (float(exp) *
                                                                                             (
                                                                                                 (float(
                                                                                                     komm) / 100))) * 0.8
        profit = lambda inc, expen: (inc - expen) * 1.27

    else:
        profit_coin = lambda time: (time * R * H) / (D * pow(2, 32))
        income = lambda incoin: exchange_rate * float(incoin) * 1.19
        expense = lambda time, exp: float(potreb) / 1000 * time * float(cost_electricity) + (float(exp) *
                                                                                             ((float(komm) / 100)))
        profit = lambda inc, expen: inc - expen

    profit_coin_hour = profit_coin(hour)
    profit_coin_day = profit_coin(day)
    profit_coin_week = profit_coin(week)
    profit_coin_month = profit_coin(month)

    income_hour = income(profit_coin_hour)
    income_day = income(profit_coin_day)
    income_week = income(profit_coin_week)
    income_month = income(profit_coin_month)

    expense_hour = expense(1, income_hour)
    expense_day = expense(24, income_day)
    expense_week = expense(168, income_week)
    expense_month = expense(720, income_month)

    profit_hour = profit(income_hour, expense_hour)
    profit_day = profit(income_day, expense_day)
    profit_week = profit(income_week, expense_week)
    profit_month = profit(income_month, expense_month)

    return "{0:.10f}".format(profit_coin_hour), "{0:.10f}".format(profit_coin_day), \
           "{0:.10f}".format(profit_coin_week), "{0:.10f}".format(profit_coin_month), \
           "{0:.2f}".format(income_hour), "{0:.2f}".format(income_day), "{0:.2f}".format(income_week), \
           "{0:.2f}".format(income_month), "{0:.2f}".format(expense_hour), "{0:.2f}".format(expense_day), \
           "{0:.2f}".format(expense_week), "{0:.2f}".format(expense_month), "{0:.2f}".format(profit_hour), \
           "{0:.2f}".format(profit_day), "{0:.2f}".format(profit_week), "{0:.2f}".format(profit_month)
