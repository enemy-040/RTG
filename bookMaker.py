import numpy as np
import pandas as pd
from ready_trader_go import order_book
from tqdm import tqdm


market_data = pd.read_csv('data/market_data2.csv')



initBook = order_book.OrderBook(
        instrument=0,
        maker_fee=0.01,
        taker_fee=0.02)

timeArr = market_data['Time'].values
operationsArr = market_data['Operation'].values
idsArr = market_data['OrderId'].values
instrumentArr = market_data['Instrument'].values
lifespanArr = market_data['Lifespan'].values
sideArr = market_data['Side'].values
priceArr = market_data['Price'].values
volumeArr = market_data['Volume'].values

for op in tqdm(range(len(market_data))):
    if operationsArr[op] == 'Insert':
       tempOrder = order_book.Order(
               client_order_id = idsArr[op],
               instrument = instrumentArr[op],
               lifespan = lifespanArr[op],
               side = sideArr[op],
               price = priceArr[op],
               volume= volumeArr[op]
               )
       initBook.insert(now=timeArr[op], order=tempOrder)

    elif operationsArr[op] == 'Amend':
        initBook.amend(
                now=timeArr[op],
                order=idsArr[op],
                new_volume=volumeArr[op])

    elif market_data['Operation'][op] == 'Cancel':
        finding = market_data[market_data['OrderId'] == market_data['OrderId'][op]]

        toCancel = order_book.Order(
               client_order_id = market_data['OrderId'][op],
               instrument = market_data['Instrument'][op],
               lifespan = market_data['Lifespan'][op],
               side = market_data['Side'][op],
               price = market_data['Price'][op],
               volume= market_data['Volume'][op]
               )
        initBook.cancel(
                now = timeArr[op],
                order = toCancel
                )



