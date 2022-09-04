from cmath import isnan, log
import pandas as pd
from tkinter.tix import MAX
import yfinance as yf
import math
import time
from threading import Thread
import os

stock_list = []
sorted_stock_list = []

class Stock:
    ticker = None
    name = None
    years = None
    data = None
    info = None

    current_price = 0
    average_growth = 0
    average_growth_percent = 0
    average_dividend = 0
    dividend_percent = 0
    average_dividend_years = 0
    price_earning_ratio = 0

    total_yield = 0
    potential_loss = 0
    risk = 0

    def __init__(self, name, years) -> None:
        self.name = name
        self.years = years

        print("\nFetching data for: " + self.name)

        self.ticker = yf.Ticker(self.name)

        thread = Thread(target=self.getInfo)
        thread.start()

        self.data = self.ticker.history(period=MAX, interval="1mo")
        self.data = self.data[::-1]

        if self.data.empty:
            return

        self.current_price = float(self.data.iloc[0].iat[3])
        print(self.name + ": Price: $" + str(self.current_price))

        (self.average_growth, self.average_growth_percent) = self.getAverageGrowth()
        self.average_dividend = self.getAverageDividend()

        if self.average_growth is None or self.average_dividend is None:
            return

        if self.average_growth < 0 or self.average_growth_percent < 50:
            print(self.name + ": Average grow is negative or growth% too low!")
            return

        self.dividend_percent = self.average_dividend / self.current_price * 100
        print(self.name + ": Dividend%: " + str(self.dividend_percent) + "%")

        self.average_dividend_years = self.average_dividend * self.years
        print(self.name + ": Dividend " + str(self.years) + "yrs: $" + str(self.average_dividend_years))

        thread.join()

        if self.info is None:
            return

        try:
            self.price_earning_ratio = self.info["trailingPE"]
            print(self.name + ": PER: " + str(self.price_earning_ratio))
        except:
            print(self.name + ": PER not found!")
            return
        
        if self.price_earning_ratio > 25:
            print(self.name + ": PER too high!")
            return

        self.total_yield = self.average_growth + self.average_dividend_years
        print(self.name + ": Yield " + str(self.years) + "yrs: $" + str(self.total_yield))

        self.potential_loss = self.current_price - self.average_dividend_years
        print(self.name + ": Potential loss " + str(self.years) + "yrs: $" + str(self.potential_loss))

        self.risk = self.potential_loss / self.total_yield
        print(self.name + ": Risk " + str(self.years) + "yrs: " + str(self.risk))

        if self.risk == 0:
            return

        stock_list.append(self)
        print(self.name + ": Was retrieved correctly!")

    def getAverageGrowth(self):
        years = self.years
        prices = []
        prices_calculated = []
        percent_prices_calculated = []
        result = 0
        result_percent = 0
        
        while_index = 0
        while len(prices) < years * 12:
            try:
                tmp = float(self.data.iloc[while_index].iat[3])
            except: break
            
            while_index += 1

            if not math.isnan(tmp):
                prices.append(tmp)

        if len(prices) >= years * 12:
            for i in range(years):
                val = prices[i] - prices[i + 12 * (years - 1)]
                if val > 0:
                    percent_prices_calculated.append(1)
                else: percent_prices_calculated.append(0)

                prices_calculated.append(prices[i] - prices[i + 12 * (years - 1)])

            for i in range(len(prices_calculated)):
                result += prices_calculated[i]

            for i in range(len(percent_prices_calculated)):
                result_percent += percent_prices_calculated[i]

            print(self.name + ": Growth " + str(years) + "yrs: $" + str(result / len(prices_calculated)))
            print(self.name + ": Growth% " + str(years) + "yrs: " + str(result_percent / len(percent_prices_calculated) * 100) + "%")

            return (result / len(prices_calculated), result_percent / len(percent_prices_calculated) * 100)

        print(self.name + ": Not enough data found!")
        return (None, None)

    def getAverageDividend(self):
        tmp = self.ticker.dividends[::-1]
        result = None

        if len(tmp) > 0 and len(tmp) >= self.years * 4:
            result = 0
            for i in range(self.years * 4):
                result += float(tmp.iloc[i])

            result = (result / (self.years * 4) * 4)
            print(self.name + ": Dividend: $" + str(result))

        if result is None:
            print(self.name + ": No dividend data found!")

        return result

    def getInfo(self):
        self.info = self.ticker.get_info()

    def toArray(self):
        return [
            self.name,
            self.years,
            round(self.current_price, 2),
            round(self.average_growth, 2),
            round(self.average_growth_percent, 2),
            round(self.average_dividend, 2),
            round(self.dividend_percent, 2),
            round(self.average_dividend_years , 2),
            round(self.price_earning_ratio, 2),
            round(self.total_yield, 2),
            round(self.potential_loss, 2),
            round(self.risk, 2)
        ]

def expandTime(seconds):
    minutes = 0
    hours = 0

    seconds = int(seconds)

    if seconds > 60:
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)

    if minutes > 60:
        hours = int(minutes / 60)
        minutes = int(minutes % 60)

    return (hours, minutes, seconds)

def getSortKey(stock):
    return stock.risk

def main():
    last_time = time.time()

    file = open("./stocklist.txt", "r")
    stock_name_list = file.read().split("\n")

    for (index, value) in enumerate(stock_name_list):
        if index > len(stock_name_list) / 250:
            break

        Stock(value, 5)

    (hours, minutes, seconds) = expandTime(time.time() - last_time)

    stock_list.sort(key=getSortKey)

    print("\nProgram finished in " + str(hours) + " hrs " + str(minutes) + " min " + str(seconds) + " seconds!")
    print("Loaded " + str(len(stock_list)) + " stocks!")

    array_stocks = []

    for (index, value) in enumerate(stock_list):
        array_stocks.append(value.toArray())

    dataframe = pd.DataFrame(array_stocks, columns=[
        "Name",
        "Years Viewed",
        "Price",
        "Average Growth",
        "Average Growth %",
        "Average Dividend",
        "Dividend %",
        "Dividend * Years",
        "PER",
        "Potential Earning",
        "Potential Loss",
        "Risk"
    ])


    excel_writer = pd.ExcelWriter("stocklist.xlsx")
    dataframe.to_excel(excel_writer, sheet_name="stocks", engine="xlsxwriter")

    for column in dataframe:
        column_width = max(dataframe[column].astype(str).map(len).max(), len(column) + 5)
        col_idx = dataframe.columns.get_loc(column)
        excel_writer.sheets["stocks"].set_column(col_idx, col_idx, column_width)

    excel_writer.save()

if __name__ == "__main__":
    os.system("pip install yfinance xlsxwriter")

    main()