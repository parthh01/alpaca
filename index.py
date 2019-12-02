from config import * 
import requests 
import alpaca_trade_api as alpaca
import matplotlib.pyplot as plt 
import pandas as pd 
import random
import math


api = alpaca.REST(api_key_id,api_secret_key,base_url=endpoint_url, api_version='v2')
account = api.get_account()


api.cancel_all_orders()
# google_order = api.submit_order('GOOGL',10,side = 'buy',type ='market',time_in_force= 'day')

tradeLimit = 4
stock_df = api.polygon.historic_agg('minute', 'GE', limit=tradeLimit).df

f_prime = [0,0]
f_2_prime = [0,0]
rowIdx = []
holding = False 
balance = 20
start_bal = balance
numBuys = 0
numSells = 0
stock = 'GE'

for i in range(tradeLimit): 
    rowIdx.append(i)
    if i >= 2: 
        f_prime.append(stock_df.iloc[i-1]['close']-stock_df.iloc[i-1]['open'])
        f_2_prime.append(f_prime[i] - f_prime[i-1])
    if holding: 
         if (round(stock_df.iloc[i]['open'],1) > buyPrice) & (f_2_prime[i] <= 0): #using 1dp so a significant profit is actually made 
             sellPrice = stock_df.iloc[i]['open']
             # api.submit_order('GE',1,side = 'sell',type ='market',time_in_force= 'day') can only use once live trading starts 
             balance += sellPrice 
             numSells +=1 
             holding = not holding
             
    else: 
        if (f_prime[i] > 0) & (f_2_prime[i] > 0):
            buyPrice = round(random.uniform(stock_df.iloc[i]['low'],stock_df.iloc[i]['high']),2)
            api.submit_order(stock,1,side = 'buy',type ='market',time_in_force= 'day')
            #shares = math.floor(balance % buyPrice)
            balance -= buyPrice
            numBuys += 1 
            holding = not holding 

if holding: 
    balance += stock_df.iloc[tradeLimit-1]['open']


stock_df['rowindex'] = rowIdx
stock_df['fprime'] = f_prime
stock_df['fdoubleprime'] = f_2_prime

print(stock_df)
print('the net margin is ',((balance-start_bal)*100/start_bal))
# print('percentage net is ',round(((balance - start_bal)*100)/start_bal,2))
print(str(numBuys) + ' buy and sell transactions completed')





# stock_df.plot(kind = 'line',x = 'rowindex',y='close',color ='red')
# plt.show()
