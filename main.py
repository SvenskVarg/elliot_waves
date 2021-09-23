from matplotlib import pyplot as plt
import pandas as pd


def read_data():
    data = pd.read_csv('HEXA-B.ST.csv', parse_dates=True)
    data.Date = pd.to_datetime(data.Date)
    return data


def plot_prices(data):
    fig, ax = plt.subplots()
    ax.plot(data.Date, data.Close)


def calculate_rsi(data, window=14):
    delta = data["Adj Close"].diff()
    up, down = delta.clip(lower=0), delta.clip(upper=0)
    roll_up = up.ewm(span=window).mean()
    roll_down = down.abs().ewm(span=window).mean()
    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    data["rsi"] = rsi
    return data


def plot_rsi(data):
    fig, ax = plt.subplots()
    ax.plot(data.Date, data.rsi)


def trading_rule(rsi, buy_rsi, sell_rsi):
    if rsi > sell_rsi:
        return "sell"
    elif rsi < buy_rsi:
        return "buy"
    else:
        return "hold"




if  __name__   ==  '__main__':
    data = read_data()
    # plt.show()
    # plot_rsi(rsi)
    # plot_prices(data)
    ending_value = []
    for buy_rsi in range(0, 101):
        shares = 0
        cash = 1000000
        rsi = calculate_rsi(data)
        for t in range(3, data.shape[0]):
            datetime =(data.loc[t, 'Date'])
            date = datetime.date()
            rsi = (data.loc[t-1, 'rsi'])
            price = data.loc[t, 'Adj Close']
            rule = trading_rule(rsi, buy_rsi, 100 - buy_rsi)
            if (rule == "buy") & (cash != 0):
                shares = cash / price
                #print("Buying! I now have", round(shares), "shares on the", date)
                cash = 0
                pass
            elif (rule == "sell") & (cash == 0):
                cash = cash + (price * shares)
                #print("Selling! I now have", round(cash,2), "cash on the", date)
                shares = 0
        final_cash = cash + (price * shares)
        shares = 0
        ending_value.append(final_cash)
        # HERE WE WANT TO SAVE THE CASH
        #print("All done! I have", round(cash,2), "dollars"
    max_cash = max(ending_value)
    max_index = ending_value.index(max_cash)
    print(max_index, max_cash)