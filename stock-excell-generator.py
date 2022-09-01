from pickle import TRUE
import sys
import yfinance as yf
from threading import Thread

stock_list = []

class Stock:
    name = None
    data = None

    def __init__(self, data, name) -> None:
        self.data = data
        self.name = name

def main():
    file = open("./stocklist.txt", "r")
    stock_name_list = file.read().split("\n")

    for (index, value) in enumerate(stock_name_list):
            tmp = yf.Ticker(value)

            print("Downloading data for: " + value)
            stock_list.append(Stock(tmp.info, value))

if __name__ == "__main__":
    main()