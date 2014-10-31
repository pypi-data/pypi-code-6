import pandas as pd

# load the national accounts data
na_data = pd.read_stata('./data/na_data.dta')

# need a swtich for Chinese data!

for var in ['c', 'i', 'g', 'x', 'm', 'gfcf']:

    # declare temporary variables
    tmp_price = 'p_' + var
    tmp_value = 'v_' + var
    tmp_quantity = 'q_' + var

    na_data[tmp_price] = na_data[tmp_value] / na_data[tmp_quantity]


# load the us trade prices data
us_trade_prices_data = pd.read_stata('./data/us_trade_prices.dta')

# merge the two data sets (applies U.S. trade data to ALL countries!)
new_data = pd.merge(na_data, us_trade_prices_data)
