from cmath import log
from concurrent.futures import thread
from pickle import TRUE
import sys
from tkinter.tix import MAX
import yfinance as yf

stock_list = []

class Stock:
    ticker = None
    name = None
    data = None

    def __init__(self, name) -> None:
        self.name = name

        ticker = yf.Ticker(self.name)
        self.data = ticker.history(period=MAX)

        print(self.data)

def main():
    file = open("./stocklist.txt", "r")
    stock_name_list = file.read().split("\n")

    for (index, value) in enumerate(stock_name_list):
        print("\nFetching data for: " + value)
        stock_list.append(Stock(value))
        

if __name__ == "__main__":
    main()