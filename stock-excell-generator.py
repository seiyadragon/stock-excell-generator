from cmath import log
from concurrent.futures import thread
from pickle import TRUE
import sys
import yfinance as yf

stock_list = []

class Stock:
    name = None
    data = None

    def __init__(self, data, name) -> None:
        self.data = data
        self.name = name

        print("$" + str(self.data["regularMarketPrice"]))

def main():
    file = open("./stocklist.txt", "r")
    stock_name_list = file.read().split("\n")

    for (index, value) in enumerate(stock_name_list):
        print("Downloading data for: " + value)

        tmp = yf.Ticker(value)
        info = tmp.info

        if info["regularMarketPrice"] != None:
            stock_list.append(Stock(info, value))
        

if __name__ == "__main__":
    main()