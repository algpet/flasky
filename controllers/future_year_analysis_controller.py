from flask import render_template

class FutureYearAnalysisController:

    def __init__(self, parameterService, tickerRateService, ticketAnalysisService , priceChangeAnalysisService, template):
        self.parameterService = parameterService
        self.tickerRateService = tickerRateService
        self.ticketAnalysisService = ticketAnalysisService
        self.priceChangeAnalysisService = priceChangeAnalysisService
        self.template = template


    def dispatch(self, request):
        tickers, from_date, till_date = self.parameterService.init_params(260)
        test_img1 = None
        test_img2 = None
        if request.method == 'POST':
            tickers, from_date, till_date = self.parameterService.process_params(request)
            tickers = tickers[0]
            if not (tickers is None or from_date is None or till_date is None):
                ticker_data = self.tickerRateService.get_rate(tickers, from_date, till_date)
                if ticker_data is not None:
                    ticker_data = self.ticketAnalysisService.analyze_dataframe(ticker_data)
                    test_img1,test_img2 = self.priceChangeAnalysisService.simmulate_price_change(ticker_data)

        return render_template(self.template, tickers=tickers, from_date=from_date, till_date=till_date,test_img1=test_img1,test_img2=test_img2)