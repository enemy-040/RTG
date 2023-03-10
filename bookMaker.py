import numpy as np
import pandas as pd
from ready_trader_go import order_book
from tqdm import tqdm


market_data = pd.read_csv('data/market_data2.csv')


Book0 = order_book.OrderBook(
        instrument=0,
        maker_fee=0.01,
        taker_fee=0.02)
Book1 = order_book.OrderBook(
    instrument=1,
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
        # print("Insert")

        tempOrder = order_book.Order(
            client_order_id=idsArr[op],
            instrument=instrumentArr[op],
            lifespan=lifespanArr[op],
            side=sideArr[op],
            price=priceArr[op],
            volume=volumeArr[op]
        )
        if instrumentArr[op] == 0:
            Book0.insert(now=timeArr[op], order=tempOrder)
        elif instrumentArr[op] == 1:
            Book1.insert(now=timeArr[op], order=tempOrder)

    elif operationsArr[op] == 'Amend':
        # print("Amend")
        if instrumentArr[op] == 0:
            Book0.amend(
                    now=timeArr[op],
                    order=idsArr[op],
                    new_volume=volumeArr[op])

        elif instrumentArr[op] == 1:
            Book1.amend(
                now=timeArr[op],
                order=idsArr[op],
                new_volume=volumeArr[op])


    elif operationsArr[op] == 'Cancel':

        orderFound = np.where(idsArr == idsArr[op])[0][0]

        toCancel = order_book.Order(
            client_order_id=idsArr[orderFound],
            instrument=instrumentArr[orderFound],
            lifespan=lifespanArr[orderFound],
            side=sideArr[orderFound],
            price=priceArr[orderFound],
            volume=volumeArr[orderFound]
        )
        if instrumentArr[op] == 0:
            Book0.cancel(
                now=timeArr[op],
                order=toCancel
            )
        elif instrumentArr[op] == 1:
            Book1.cancel(
                now=timeArr[op],
                order=toCancel
            )




