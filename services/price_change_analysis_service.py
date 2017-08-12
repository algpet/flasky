import scipy.stats as sct
import random
import math


from matplotlib import use
use("Agg")
import matplotlib.pyplot as plt


class PriceChangeAnalysisService:

    def __init__(self,volatilityAnalysisService):
        self.volatilityAnalysisService = volatilityAnalysisService

    def calculate_price_change(self,df):

        last_close = df.iloc[0]['Close']
        volatilities = self.volatilityAnalysisService.calculate_volatility(df)

        expected_monthly_shift = last_close * volatilities['month'] / 100
        expected_yearly_shift  = last_close * volatilities['year']  / 100

        expected_monthly_grow = last_close + expected_monthly_shift
        expected_monthly_drop = last_close - expected_monthly_shift
        expected_yearly_grow = last_close + expected_yearly_shift
        expected_yearly_drop = last_close - expected_yearly_shift

        return {
            "last_close":last_close,
            "expected_monthly_grow":round(expected_monthly_grow,2),
            "expected_monthly_drop":round(expected_monthly_drop,2),
            "expected_yearly_grow":round(expected_yearly_grow,2),
            "expected_yearly_drop":round(expected_yearly_drop,2)
        }


    #just quick and dirty verion ...
    def simmulate_price_change(self,df):

        import glob
        import os

        files = glob.glob('static/img/*.png')
        for filename in files:
            os.unlink(filename)


        filename1 = "static/img/graph" + str(random.randint(100000000, 999999999)) + ".png"
        filename2 = "static/img/graph" + str(random.randint(100000000, 999999999)) + ".png"

        last_close = df.iloc[0]['Close']

        #calculate mean for last year

        year_df = df[0:251]["Close"]
        avg = year_df.mean()
        stdev = year_df.std()


        price = last_close

        graph_xlab = [-1.5]
        graph_x = [0]
        graph_y = [price]
        for iter in range(16):
            devi = stdev * price / avg
            price = sct.norm.ppf(random.random(), price, devi)
            graph_y.append(round(price,2))
            graph_x.append(3 * (iter + 1))
            graph_xlab.append(3 * (iter + 0.5))

        plt.clf()
        plt.plot()
        plt.xlabel('weeks')
        plt.ylabel('price')
        plt.plot(graph_x, graph_y, color="#FF0000",markersize=4,marker="o")

        plt.xticks(graph_x)

        font = {'family': 'normal',
                'size': 7}
        ylim = plt.ylim()
        xlim = plt.xlim()
        axes = plt.gca()
        axes.set_ylim([ylim[0] - 5, ylim[1] + 5])
        axes.set_xlim([xlim[0] - 1.5 , xlim[1]])
        bot = plt.ylim()[0] * 1.02

        colors = ["green","blue"]
        for i in range(len(graph_x)):
            plt.text(graph_xlab[i], bot , str(graph_y[i]), fontdict=font , color= colors[i % 2])
        plt.savefig(filename1)


        final_prices = []
        devi = stdev * price / avg
        for fp in range(100):
            final_price = sct.norm.ppf(random.random(), price, devi)
            final_prices.append(round(final_price,2))

        stdev_archetypes = {-3:0 , -2:0 , -1:0 , 0:0 , 1:0 , 2:0 , 3:0}
        for price in final_prices:
            ac = (price - last_close) / stdev
            ac = math.trunc(ac)
            if ac < -4:
                ac = -4
            if ac > 3:
                ac = 3

            if ac not in stdev_archetypes:
                stdev_archetypes[ac] = 0
            stdev_archetypes[ac] += 1

        keys = stdev_archetypes.keys()
        keys2 = []
        for key in keys:
            keys2.append(key + 0.25)

        plt.clf()
        plt.plot()
        plt.xlabel('stdevs away from avg')
        plt.ylabel('count of simmulations')
        plt.bar(keys2, stdev_archetypes.values(), 0.5, color='r')
        plt.savefig(filename2)


        return filename1,filename2,final_prices



