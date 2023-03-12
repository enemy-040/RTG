import numpy as np
from arch import arch_model
from sklearn.model_selection import train_test_split

a_s_arr = np.load('data/a_std.npy')
a_mn_arr = np.load('data/a_mn.npy')
b_s_arr = np.load('data/b_std.npy')
b_mn_arr = np.load('data/b_mn.npy')

# study of volatility
ask_std_train, ask_std_test, bid_std_train, bid_std_test = train_test_split(
        a_s_arr,
        b_s_arr,
        train_size=0.8,
        test_size=.2,
        random_state=69
        )

a_s_model = arch_model(
        ask_std_train,
        p=20
        ).fit(disp='off')

b_s_model = arch_model(
        bid_std_train,
        p=20
        ).fit(disp='off')


# study of mean
ask_mn_train, ask_mn_test, bid_mn_train, bid_mn_test = train_test_split(
        a_mn_arr,
        b_mn_arr,
        train_size=0.8,
        test_size=.2,
        random_state=69
        )

a_m_model = arch_model(
        ask_mn_train,
        p=20
        ).fit(disp='off')


b_m_model = arch_model(
        bid_mn_train,
        p=20
        ).fit(disp='off')



#extracting coefficients

print(f"coefs of a_s_model = {a_s_model.params}")
print(f"coefs of a_s_model = {b_s_model.params}")
print(f"coefs of a_s_model = {a_m_model.params}")
print(f"coefs of a_s_model = {b_m_model.params}")
