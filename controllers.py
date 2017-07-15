from flask import Flask
from flask import request
from flask import render_template

from stock_rate_service import TickerRateService
from ticker_info_service import TickerInfoService
from params_service import ParameterService

tickerRateService = TickerRateService('google')
tickerNameService = TickerInfoService('secwiki_tickers.csv')
parameterService = ParameterService(10)
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def request_form():
    ticker_data = None
    ticker_headers = None

    tickers, from_date, till_date = parameterService.init_params()
    if request.method == 'POST':
        tickers, from_date, till_date = parameterService.process_params(request)
        if not ( tickers is None or from_date is None or till_date is None):
            ticker_data = tickerRateService.get_rates(tickers, from_date, till_date)
            ticker_headers = tickerNameService.get_tickers_data(tickers)
            tickers = ",".join(tickers)

    return render_template('layout1.html', ticker_data=ticker_data, ticker_headers=ticker_headers,from_date=from_date,
                           till_date=till_date, tickers=tickers)

if __name__ == "__main__":
    app.run(debug=True, port=4999)


