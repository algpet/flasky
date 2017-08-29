from flask import render_template
class OptionsController:
    def __init__(self,parameterService,option_suggestion_service,template):
        self.parameterService = parameterService
        self.option_suggestion_service = option_suggestion_service
        self.template = template

    def dispatch(self, request):
        df_call = None
        df_put = None
        underlyingPrice, marketPrice , days, volatility,interest, dividend = self.parameterService.init_option_controller_params()

        if request.method == 'POST':
            underlyingPrice, marketPrice , days, volatility,interest, dividend = self.parameterService.process_options_params(request)
            df_call , df_put = self.option_suggestion_service.calculate_options(underlyingPrice,days,volatility,interest,dividend,marketPrice)

        return render_template(self.template,underlyingPrice=underlyingPrice,marketPrice=marketPrice,
                               days=days,volatility=volatility,interest=interest,dividend=dividend,
                               df_call=df_call,df_put=df_put)

