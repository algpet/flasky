
class TickerInfoService():
    def __init__(self,source_file):
        self.data = {}
        file = open(source_file)
        for line in file:
            info = line.split(",")
            self.data[info[0].capitalize()] = {"name":info[1] }

    def get_ticker_data(self,ticker):
        return self.data[ticker.capitalize()]

    def get_tickers_data(self,tickers):
        data = {}
        for ticker in tickers:
            data[ticker] = self.get_ticker_data(ticker)
        return data