from cmath import isnan, log
from concurrent.futures import thread
from inspect import getargvalues
from pickle import FALSE, TRUE
import sys
from tkinter.tix import MAX
import yfinance as yf
import math

stock_list = []

class Stock:
    ticker = None
    name = None
    years = None
    data = None

    current_price = None
    average_growth = None
    average_dividend = None
    price_earning_ratio = None

    total_yield = None
    potential_loss = None
    risk = None

    def __init__(self, name, years) -> None:
        self.name = name
        self.years = years

        print("\nFetching data for: " + self.name)

        self.ticker = yf.Ticker(self.name)
        self.data = self.ticker.history(period=MAX, interval="1mo")
        self.data = self.data[::-1]

        if self.data.empty:
            stock_list.pop(len(stock_list) - 1)
            return
        
        self.current_price = float(self.data.iloc[0].iat[3])
        print(self.name + ": $" + str(self.current_price))

        self.average_growth = self.getAverageGrowth()
        self.average_dividend = self.getAverageDividend()
        print(self.ticker.actions)

        print(self.name + ": Was retrieved correctly!")

    def getAverageGrowth(self):
        years = self.years
        prices = []
        prices_calculated = []
        result = 0
        range_offset = 0
        
        while_index = 0
        while len(prices) < years * 12:
            try:
                tmp = float(self.data.iloc[while_index].iat[3])
            except: break
            
            while_index += 1

            if not math.isnan(tmp):
                prices.append(tmp)

        print(self.name + ": Months found --" + str(len(prices)))

        if len(prices) >= years * 12:
            for i in range(years):
                prices_calculated.append(prices[i] - prices[i + 12 * (years - 1)])

            for i in range(len(prices_calculated)):
                result += prices_calculated[i]

            print(self.name + ": " + str(result / len(prices_calculated)))

            return result / len(prices_calculated)


        return "Not enough data!"

    def getAverageDividend(self):
        tmp = self.ticker.dividends[::-1]
        result = 0

        if len(tmp) > 0 and len(tmp) >= self.years * 4:
            for i in range(self.years * 4):
                result += float(tmp.iloc[i])

            result = (result / (self.years * 4))

        print(self.name + ": " + str(result))
        return result

def exportToExcell():
    pass            

def main():
    file = open("./stocklist.txt", "r")
    stock_name_list = file.read().split("\n")

    for (index, value) in enumerate(stock_name_list):
        stock_list.append(Stock(value, 5))
        

if __name__ == "__main__":
    main()