from config import *
import requests 
import alpaca_trade_api as alpaca 
import math 
import numpy as np
import random
import urllib.request 
import time 
from bs4 import BeautifulSoup


######Notes ###### 
# implement taylor series approximation to determine price of stock in the next minute using accumulated stock data
# to find the nth derivative of a point x = f(t) you need n+1 datapoints, or n datapoints prior to x = f(t)
# have to use a dp approach to find the sum of taylor series terms 
# for us the timestep term is always 1 so the formula turns out to be: 
# formula  = F(a) + SIGMA ( f_n(a)/n!) 



get_stock()

    # stock_df['prediction'] = prediction

##### everything below was commented out #### 

# stock_df = api.polygon.historic_agg('minute', ticker, limit=limit).df


# #calculalting derivatives: 
# #  create an array of size (n rows, n-1 cols )
# # for each row, or price, calculate all the derivatives across 

# derivatives = np.zeros([len(stock_df),len(stock_df)]) 
# sum_taylor = []
# holding = False 
# start_bal = 300
# bank = start_bal

# for i in range(len(stock_df)): 
#     derivatives[i][0] = stock_df.iloc[i]['close']
#     if i > 0: 
#         for j in range(1,i): 
#             derivatives[i][j] = (derivatives[i][j-1] - derivatives[i-1][j-1])/math.factorial(j) # just changed this to the actual term
#     sum_taylor.append(np.sum(derivatives[i][1:len(derivatives[i])]))
#     if holding: 
#         if (sum_taylor[i] < 0) & (stock_df.iloc[i]['open'] > buyPrice): 
#             sellPrice = round(random.uniform(stock_df.iloc[i]['low'],stock_df.iloc[i]['high']),2)
#             bank += sellPrice 
#             holding = not holding 
#     else: 
#         if sum_taylor[i] > 0: 
#             buyPrice = round(random.uniform(stock_df.iloc[i]['low'],stock_df.iloc[i]['high']),2) 
#             api.submit_order(ticker,1,side = 'buy',type ='market',time_in_force= 'day')
#             bank -= buyPrice 
#             holding = not holding 

# if holding: 
#     sellPrice = round(random.uniform(stock_df.iloc[len(stock_df)-1]['low'],stock_df.iloc[len(stock_df)-1]['high']),2)
#     bank += sellPrice

# # 1 is true prediction, 0 is false prediction, 2 is no change predicted




# print(stock_df)
# print('accuracy was ',prediction.count(1)*100/(len(prediction)-1), ' percent')
        





