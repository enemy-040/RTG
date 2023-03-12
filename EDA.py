import pandas as pd
import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
#from arch import arch_model
from sklearn.model_selection import train_test_split




def getPriceVolArr(book:np.ndarray)-> Tuple[np.array, np.array]:
    askVolPriceProd = np.array([])
    bidVolPriceProd = np.array([])

    for volumeIt in range(len(book['ask_volumes'])):
        askVolPriceProd = np.concatenate(
                (askVolPriceProd,
                 [book["ask_prices"][volumeIt] for t in range(book['ask_volumes'][volumeIt])]),
                axis=None
            )

    for volumeIt in range(len(book['bid_volumes'])):
        bidVolPriceProd = np.concatenate(
                (bidVolPriceProd,
                [book["bid_prices"][volumeIt] for t in range(book["bid_volumes"][volumeIt])]),
                axis=None
            )
    return askVolPriceProd, bidVolPriceProd



def getMnVarAtTime(book:np.ndarray) -> Tuple[np.array, np.array, np.array, np.array]:
    ask_Std = np.empty(len(book))
    bid_Std = np.empty(len(book))
    ask_mn = np.empty(len(book))
    bid_mn = np.empty(len(book))
    for i in range(len(book)):
        askVPP, bidVPP = getPriceVolArr(book[i][0])
        ask_Std[i] = np.sqrt(np.var(askVPP)) if len(askVPP) != 0 else 0
        ask_mn[i] = np.mean(askVPP) if len(askVPP) !=0 else 0
        bid_Std[i] = np.sqrt(np.var(bidVPP)) if len(bidVPP) != 0 else 0
        bid_mn[i] = np.mean(bidVPP) if len(bidVPP) != 0 else 0

    return ask_Std, ask_mn, bid_Std, bid_mn


book = pd.read_json('data/books.json').values
#%%


ask_Std_Arr, ask_mn_Arr, bid_Std_Arr, bid_mn_Arr = getMnVarAtTime(book)

plt.plot(bid_Std_Arr)
plt.plot(ask_Std_Arr)
plt.savefig('stdvPlt.png')

plot_acf(bid_Std_Arr)
plot_pacf(bid_Std_Arr)

plot_acf(ask_Std_Arr)
plot_pacf(ask_Std_Arr)

ask_std_train, ask_std_test, bid_std_train, bid_std_test = train_test_split(
        ask_Std_Arr,
        bid_Std_Arr,
        train_size=0.8,
        test_size=.2,
        random_state=69
        )

#model = arch_model(train, mean='Zero', vol='GARCH', p=6, q=#tbd take variance of variance)
exp_var = {}
for i in range(1, 10):
    exp_var[i] = pd.Series(ask_std_train).rolling(window=i+2).var()

print(exp_var)

