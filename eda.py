import pandas as pd
import numpy as np
from typing import Tuple
import os
from tqdm import tqdm


def getPriceVolArr(book:np.ndarray)-> Tuple[np.array, np.array]:
    askVolPriceProd = np.array([])
    bidVolPriceProd = np.array([])

#    for volumeIt in range(len(book['ask_volumes'])):
#        askVolPriceProd = np.concatenate(
#                (askVolPriceProd,
#                 [book["ask_prices"][volumeIt] for t in range(book['ask_volumes'][volumeIt])]),
#                axis=None
#            )

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
    for i in tqdm(range(len(book))):
        askVPP, bidVPP = getPriceVolArr(book[i][0])
        #ask_Std[i] = np.sqrt(np.var(askVPP)) if len(askVPP) != 0 else 0
        #ask_mn[i] = np.mean(askVPP) if len(askVPP) !=0 else 0
        bid_Std[i] = np.sqrt(np.var(bidVPP)) if len(bidVPP) != 0 else 0
        bid_mn[i] = np.mean(bidVPP) if len(bidVPP) != 0 else 0

    return ask_Std, ask_mn, bid_Std, bid_mn

book = pd.read_json('books.json').values
ask_Std_Arr, ask_mn_Arr, bid_Std_Arr, bid_mn_Arr = getMnVarAtTime(book)

cwd = os.getcwd()
#np.save(os.path.join(cwd,'data/a_std.npy'), ask_Std_Arr)
#np.save(os.path.join(cwd,'data/a_mn.npy'), ask_mn_Arr)
np.save(os.path.join(cwd,'data/b_std.npy'),bid_Std_Arr)
np.save(os.path.join(cwd,'data/b_mn.npy'), bid_mn_Arr)

