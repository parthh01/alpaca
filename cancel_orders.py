from config import *
import alpaca_trade_api as alpaca 

api = alpaca.REST(api_key_id,api_secret_key,base_url=endpoint_url, api_version='v2')
api.cancel_all_orders()



print(api.get_clock().is_open)

# api.submit_order('AAPL',1,side = 'buy',type ='market',time_in_force= 'ioc')
