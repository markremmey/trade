from alpaca.data.live import CryptoDataStream
from talipp.indicators import EMA, ATR
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()


ALPACA_KEY = os.getenv("API_KEY")
ALPACA_SECRET = os.getenv("API_SECRET")

client = CryptoDataStream(ALPACA_KEY, ALPACA_SECRET)

bars = []

ema_2 = EMA(period = 2)
ema_4 = EMA(period = 4)
atr = ATR(period = 2)

async def bar_handler(data):
    print(f"hi {datetime.now()} {data")
    ema_2.add_input_value(data.close)
    ema_4.add_input_value(data.close)
    print(ema_2, ema_4)

    atr.add_input_value(data)

    print(atr)

client.subscribe_bars(bar_handler, "BTC/USD")

client.run()
print(ALPACA_KEY)
print(ALPACA_SECRET)