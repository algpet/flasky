from datetime import date, timedelta

class ParameterService:

    def __init__(self,default_date_gap=10):
        self.default_date_gap = default_date_gap
        self.default_ticker = ""

    def init_params(self,date_gap=None):
        if date_gap is None:
                date_gap = self.default_date_gap
        return self.default_ticker , date.today() - timedelta(days=date_gap), date.today()

    def process_params(self,request):
        from_date = request.form.get('from_date')
        till_date = request.form.get('till_date')
        tickers = request.form.get('tickers')
        if tickers is not None:
            for separator in ":,+":
                if tickers.find(separator) >= 0:
                    tickers = tickers.split(separator)
                    break
            else:
                tickers = [tickers]

        return tickers, from_date, till_date

    def get_param(self,request,param):
        return request.form.get(param)

    def init_option_controller_params(self):
        underlyingPrice = 14.00
        marketPrice = 2.2
        days = 21
        volatility = 76.5
        interest = 1.5
        dividend = 0.0
        return underlyingPrice,marketPrice,days,volatility,interest,dividend

    def process_options_params(self,request):
        underlyingPrice = float(request.form.get('underlyingPrice'))
        marketPrice = float(request.form.get('marketPrice'))
        days = int(request.form.get('days'))
        volatility = float(request.form.get('volatility'))
        interest = float(request.form.get('interest'))
        dividend = float(request.form.get('dividend'))
        return underlyingPrice, marketPrice , days, volatility, interest, dividend