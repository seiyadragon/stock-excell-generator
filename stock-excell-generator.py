from cmath import log
from concurrent.futures import thread
from inspect import getargvalues
from pickle import FALSE, TRUE
import sys
from tkinter.tix import MAX
import yfinance as yf

stock_list = []

class Stock:
    ticker = None
    name = None
    data = None
    percent_up = None

    def __init__(self, name) -> None:
        self.name = name

        ticker = yf.Ticker(self.name)
        self.data = ticker.history(period=MAX, interval="1mo")
        self.data = self.data[::-1]

        if self.data.empty:
            stock_list.pop(len(stock_list) - 1)
            return

        self.percent_up = self.getAverageTrend(5)

        print(self.name + ": Was retrieved correctly!")
        print(self.name + ": " + str(self.percent_up) + "%")

    def getAverageTrend(self, years):
        prices = []
        has_enough_data = False
        prices_calculated = []
        result = 0

        for i in range(years * 12):
            try:
                prices.append(self.data.iloc[i].iat[3])
                has_enough_data = True
            except:
                print(self.name + ": Does not have sufficient data!")
                has_enough_data = False

        print(self.name + ": Months found --" + str(len(prices)))

        if has_enough_data:
            for i in range(years):
                if prices[i] - prices[i + 12 * (years - 1)] > 0:
                    prices_calculated.append(1)
                else: prices_calculated.append(-1)

            for i in range(len(prices_calculated)):
                result += prices_calculated[i]

            return float(result / len(prices_calculated) * 100)

        return "Not enough data!"

def exportToExcell():
    pass            

def main():
    file = open("./stocklist.txt", "r")
    stock_name_list = file.read().split("\n")

    for (index, value) in enumerate(stock_name_list):
        print("\nFetching data for: " + value)
        stock_list.append(Stock(value))
        

if __name__ == "__main__":
    main()