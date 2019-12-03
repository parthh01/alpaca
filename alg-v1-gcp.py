import alpaca_trade_api as alpaca 
import requests 
from bs4 import BeautifulSoup
import numpy as np
import math 
import random
import time 
import urllib.request 
from bs4 import BeautifulSoup

def get_stock():
    api = alpaca.REST(api_key_id,api_secret_key,base_url=endpoint_url, api_version='v2')
    # account = api.get_account()

    ############################ the scraping section ############################

    stocks = []
    predictability = []

    url = "https://www.tradingview.com/markets/stocks-usa/market-movers-active/"
    response = requests.get(url)

    soup = BeautifulSoup(response.text,"html.parser")
    table = soup.find_all('a',class_='tv-screener__symbol')
    for tag in table: 
        if tag.string.isupper(): 
            stocks.append(tag.string)

    num_stocks = 10
    stocks = stocks[0:num_stocks]
    stocks.extend(['AAPL','FB'])
    limit = 170

    for stock in stocks: 
        stock_df = api.polygon.historic_agg('minute',stock, limit=limit).df
        derivatives = np.zeros([len(stock_df),len(stock_df)]) 
        sum_taylor = []
        for i in range(len(stock_df)): 
            derivatives[i][0] = stock_df.iloc[i]['close']
            if i > 0: 
                for j in range(1,i): 
                    derivatives[i][j] = (derivatives[i][j-1] - derivatives[i-1][j-1])/math.factorial(j) # just changed this to the actual term
            sum_taylor.append(np.sum(derivatives[i][1:len(derivatives[i])])) 
        stock_df['sum_taylor'] = sum_taylor
        prediction = [2]
        for i in range(1,len(stock_df)-1): 
            if stock_df.iloc[i]['sum_taylor'] > 0: 
                if stock_df.iloc[i+1]['high'] > stock_df.iloc[i]['close']: 
                    prediction.append(1)
                else: 
                    prediction.append(0)
            elif stock_df.iloc[i]['sum_taylor'] < 0: 
                if stock_df.iloc[i+1]['low'] < stock_df.iloc[i]['close']: 
                    prediction.append(1)
                else: 
                    prediction.append(0)
            else: 
                prediction.append(2)
        prediction.append(2)
        accuracy = prediction.count(1)*100/(len(prediction)-1)
        # string  = stock + ' accuracy is ' + str(accuracy)
        # print(string)
        predictability.append(accuracy)
        pos = predictability.index(max(predictability))
    return stocks[pos]


api_key_id = 'PKLKTLTTS2X68EQUKOR3'
api_secret_key = 'FrERKfP9Lt/RtC9Y8vJXFyhc9qKShrZjzxo5qD0E'
endpoint_url = 'https://paper-api.alpaca.markets'



api = alpaca.REST(api_key_id,api_secret_key,base_url=endpoint_url, api_version='v2')


############################ the alpaca section ############################

api.cancel_all_orders()
account = api.get_account()

ticker  = get_stock()
limit = 170
order_size = 1 

stock_df = api.polygon.historic_agg('minute', ticker, limit=limit).df

derivatives = np.zeros([len(stock_df),len(stock_df)]) 
sum_taylor = []
holding = False 
start_bal = float(account.daytrading_buying_power)

for i in range(len(stock_df)): 
    derivatives[i][0] = stock_df.iloc[i]['close']
    if i > 0: 
        for j in range(1,i): 
            derivatives[i][j] = (derivatives[i][j-1] - derivatives[i-1][j-1])/math.factorial(j) # just changed this to the actual term
    sum_taylor.append(np.sum(derivatives[i][1:len(derivatives[i])]))


# order_id = api.submit_order('ACB',1,side = 'buy',type ='market',time_in_force= 'day').id
# time.sleep(1)
# print(api.get_order(order_id).filled_avg_price)


while api.get_clock().is_open: 
    if holding: 
        if  (api.polygon.last_quote(ticker).askprice > float(buy_price)) : 
            order_id = api.submit_order(ticker,order_size,side = 'sell',type='limit',limit_price=float(buy_price)+0.01,time_in_force = 'day').id
            while api.get_order(order_id).filled_avg_price is None:
                time.sleep(1)
            holding = not holding 
            print('sold')
    else: 
        if sum_taylor[-1] > 0 : 
            order_id = api.submit_order(ticker,order_size,side = 'buy',type ='market',time_in_force= 'day').id
            time.sleep(1)
            buy_price = api.get_order(order_id).filled_avg_price
            holding = not holding 
            print('bought')
        else: 
            ticker = get_stock()
            stock_df = api.polygon.historic_agg('minute', ticker, limit=limit).df
            derivatives = np.zeros([len(stock_df),len(stock_df)]) 
            sum_taylor = []
            for i in range(len(stock_df)): 
                derivatives[i][0] = stock_df.iloc[i]['close']
                if i > 0: 
                    for j in range(1,i): 
                        derivatives[i][j] = (derivatives[i][j-1] - derivatives[i-1][j-1])/math.factorial(j) # just changed this to the actual term
                sum_taylor.append(np.sum(derivatives[i][1:len(derivatives[i])]))
    time.sleep(1)

net = start_bal - float(account.daytrading_buying_power)

print('start bal was ', start_bal)
