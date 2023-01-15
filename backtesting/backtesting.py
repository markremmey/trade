import vectorbt as vbt

import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()

ALPACA_KEY = os.getenv("API_KEY")
ALPACA_SECRET = os.getenv("API_SECRET")

vbt.settings.data['alpaca']['key_id']=ALPACA_KEY
vbt.settings.data['alpaca']['secret_key']=ALPACA_SECRET

price = vbt.AlpacaData.download('BTCUSD').get('Close')

fast_ma=vbt.MA.run(price, 10)
slow_ma = vbt.MA.run(price, 50)
entries= fast_ma.ma_crossed_above(slow_ma)
exits = fast_ma.ma_crossed_below(slow_ma)

pf = vbt.Portfolio.from_signals(price, entries, exits, init_cash=100)
pf.plot()