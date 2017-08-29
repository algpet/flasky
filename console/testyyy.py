from services.option_suggestion_service import OptionSuggestionService
import math
import pandas as pd



pd.set_option('display.line_width', 150)


oss = OptionSuggestionService()


underlyingPrice = 14.00
exercisePrice = 11.50
time = 21/365
interest = 1.5 * 0.01
volatility = 76.5 * 0.01
dividend = 0 * 0.01


oss.calculate_options(underlyingPrice,21,volatility,interest,dividend)


