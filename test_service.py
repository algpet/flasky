from stock_rate_service import TickerRateService

from datetime import date
from datetime import datetime, timedelta

DATE_FROM = date(2017, 3, 3)
DATE_TO = date(2017, 3, 6)

service = TickerRateService('google')

print service.get_rates('GOOGL',DATE_FROM,DATE_TO)

print service.get_rates('AAPL',DATE_FROM,DATE_TO)

stocks = ['ORCL', 'TSLA', 'IBM','YELP', 'MSFT']

print service.get_rates(stocks,DATE_FROM,DATE_TO)

print (123)