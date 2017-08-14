import matplotlib
matplotlib.use('Agg')

from services.ticker_analysis_service import TickerAnalysisService
from services.params_service import ParameterService
from services.ticker_info_service import TickerInfoService
from services.stock_rate_service import TickerRateService
from services.bullish_vs_bearish_analysis_service import BullishVsBearishAnalysisService
from services.linear_regression_service import LinearRegressionSerice
from services.volatility_analysis_service import VolatilityAnalysisService
from services.price_change_analysis_service import PriceChangeAnalysisService
from services.plotting_util_service import PlottingUtilServce
from services.price_change_simulation_service import PriceChangeSimulationService

from controllers.raw_request_controller import RawRequestController
from controllers.four_year_analysis_controller import  FourYearAnalysisController
from controllers.future_year_analysis_controller import FutureYearAnalysisController



def application_context_builder():
    tickerRateService = TickerRateService('google')
    tickerNameService = TickerInfoService('resources/secwiki_tickers.csv')
    parameterService = ParameterService(10)
    tickerAnalysisService = TickerAnalysisService()
    bullishVsBearishAnalysisService = BullishVsBearishAnalysisService()
    linearRegressionSerice = LinearRegressionSerice()
    volatilityAnalysisService = VolatilityAnalysisService()
    plottingUtilService = PlottingUtilServce()

    priceChangeAnalysisService = PriceChangeAnalysisService(volatilityAnalysisService)
    priceChangeSimulationService = PriceChangeSimulationService(volatilityAnalysisService,plottingUtilService)

    rawRequestController = RawRequestController(parameterService,tickerRateService,tickerAnalysisService, tickerNameService, "iteration1and2.html")
    fourYearAnalysisController = FourYearAnalysisController(parameterService,tickerRateService,tickerAnalysisService,
                                                            bullishVsBearishAnalysisService, linearRegressionSerice,
                                                            priceChangeAnalysisService, "iteration3andProbably4.html")

    futureYearAnalysisController = FutureYearAnalysisController(parameterService,tickerRateService,tickerAnalysisService,priceChangeSimulationService, "iteration5.html")


    return rawRequestController , fourYearAnalysisController , futureYearAnalysisController