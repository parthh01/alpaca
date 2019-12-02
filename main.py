from config import * 
import alpaca_trade_api as alpaca 
import math 
import numpy as np
import random
import time 
import requests 
import urllib.request 
from bs4 import BeautifulSoup

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


# order_id = api.submit_order('ACB',1,side = 'buy',type ='market',time_in_force= 'day').id
# time.sleep(1)
# print(api.get_order(order_id).filled_avg_price)


while api.get_clock().is_open: 
    for i in range(len(stock_df)): 
        derivatives[i][0] = stock_df.iloc[i]['close']
        if i > 0: 
            for j in range(1,i): 
                derivatives[i][j] = (derivatives[i][j-1] - derivatives[i-1][j-1])/math.factorial(j) # just changed this to the actual term
        sum_taylor.append(np.sum(derivatives[i][1:len(derivatives[i])]))
    if holding: 
        if (sum_taylor[-1] < 0) & (float(buy_price) <= api.polygon.last_quote(ticker).askprice): 
            order_id = api.submit_order(ticker,order_size,side = 'sell',type='market',time_in_force = 'day')
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

net = start_bal - float(account.daytrading_buying_power)

print('start bal was ', start_bal)

#################NOTES##########################
# 11/29
# UGAZ was trading at -20% levels, so alg was hanging after buying and waiting for sell point, which would have never kicked in so 
# stop loss needs to incorporated 
# could be because its an ETF, possibly wouldn't occur with stocks although defo possible. 
# alg was predicting 89% accuracy, so issue may be the execution logic. changed sell logic to when buy_price is equal to as well, 
# to get more cash out points 
# correlation between volume and predictability exists but is not strong, figure out how to quantify the link 
# Essentially, the strategy is similar to SMA compare, although that may be more robust 
# look into shorting stock, since the strategy is supposedly upto 89% accurate  
