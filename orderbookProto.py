import numpy as np
import pandas as pd
from ready_trader_go import order_book
from tqdm import tqdm

# Load market data
market_data = pd.read_csv('data/market_data2.csv')

# Initialize order books
book0 = order_book.OrderBook(instrument=0, maker_fee=0.01, taker_fee=0.02)
book1 = order_book.OrderBook(instrument=1, maker_fee=0.01, taker_fee=0.02)

# Initialize dictionaries to store the last order book for each time point
book0_last = {}
book1_last = {}

# Iterate over market data and update order books
for i, row in tqdm(market_data.iterrows(), total=len(market_data)):
    time = row['Time']
    operation = row['Operation']
    instrument = row['Instrument']
    order_id = row['OrderId']
    lifespan = row['Lifespan']
    side = row['Side']
    price = row['Price']
    volume = row['Volume']

    if operation == 'Insert':
        order = order_book.Order(client_order_id=order_id, instrument=instrument, lifespan=lifespan,
                                 side=side, price=price, volume=volume)
        if instrument == 0:
            book0.insert(now=time, order=order)
            book0_last[time] = book0
        elif instrument == 1:
            book1.insert(now=time, order=order)
            book1_last[time] = book1

    elif operation == 'Amend':
        if instrument == 0:
            book0.amend(now=time, order=order_id, new_volume=volume)
            book0_last[time] = book0
        elif instrument == 1:
            book1.amend(now=time, order=order_id, new_volume=volume)
            book1_last[time] = book1

    elif operation == 'Cancel':
        order_found = np.where(market_data['OrderId'] == order_id)[0][0]
        order = order_book.Order(client_order_id=order_id, instrument=instrument, lifespan=lifespan,
                                 side=side, price=price, volume=volume)
        if instrument == 0:
            book0.cancel(now=time, order=order)
            book0_last[time] = book0
        elif instrument == 1:
            book1.cancel(now=time, order=order)
            book1_last[time] = book1

#%%
print(book1_last[0.006542])