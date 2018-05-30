# -*- coding: utf-8 -*-
import datetime
from matplotlib.pylab import date2num
import matplotlib.pyplot as plt
from futuquant import OpenQuoteContext
from futuquant import OpenHKTradeContext, OpenUSTradeContext
import matplotlib.finance as mpf


class MACD(object):
    """
    A simple MACD strategy
    """
    # API parameter setting
    api_svr_ip = '127.0.0.1'  # 账户登录的牛牛客户端PC的IP, 本机默认为127.0.0.1
    api_svr_port = 11111  # 富途牛牛端口，默认为11111
    unlock_password = "Dx1111"  # 美股和港股交易解锁密码
    trade_env = 1  # 0: 真实交易 1: 仿真交易（仿真交易无密码验证，美股暂不支持仿真）

    # def myMACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    #     ewma12 = pd.ewma(prices, span=fastperiod)
    #     ewma60 = pd.ewma(prices, span=slowperiod)
    #     dif = ewma12 - ewma60
    #     dea = pd.ewma(dif, span=signalperiod)
    #     bar = (dif - dea)  # 有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    #     return dif, dea, bar

    def __init__(self, stock, short_period, long_period, smooth_period, observation):
        """
        Constructor
        """
        self.stock = stock
        self.short_period = short_period
        self.long_period = long_period
        self.smooth_period = smooth_period
        self.observation = observation
        self.quote_ctx, self.trade_ctx = self.context_setting()

    def context_setting(self):
        """
        API trading and quote context setting
        :returns: trade context, quote context
        """
        if self.unlock_password == "":
            raise Exception("请先配置交易解锁密码! password: {}".format(self.unlock_password))

        quote_ctx = OpenQuoteContext(host=self.api_svr_ip, port=self.api_svr_port)

        if 'HK.' in self.stock:
            trade_ctx = OpenHKTradeContext(host=self.api_svr_ip, port=self.api_svr_port)
            if self.trade_env == 0:
                ret_code, ret_data = trade_ctx.unlock_trade(self.unlock_password)
                if ret_code == 0:
                    print('解锁交易成功!')
                else:
                    print("请求交易解锁失败, 请确认解锁密码! password: {}".format(self.unlock_password))
        elif 'US.' in self.stock:
            if self.trade_env != 0:
                raise Exception("美股交易接口不支持仿真环境 trade_env: {}".format(self.trade_env))
            trade_ctx = OpenUSTradeContext(host=self.api_svr_ip, port=self.api_svr_port)
        else:
            raise Exception("stock输入错误 stock: {}".format(self.stock))

        return quote_ctx, trade_ctx

    def handle_data(self):
        """
        handle stock data for trading signal, and make order
        """
        # 读取历史数据，使用sma方式计算均线准确度和数据长度无关，但是在使用ema方式计算均线时建议将历史数据窗口适当放大，结果会更加准确
        # today = datetime.datetime.today()
        today = datetime.datetime.strptime('2018-04-10', '%Y-%m-%d')
        pre_day = (today - datetime.timedelta(days=self.observation)).strftime('%Y-%m-%d')
        pre_day = '2018-01-01'
        _, prices = self.quote_ctx.get_history_kline(self.stock, start=pre_day)
        # print(prices)
        # macd, signal, hist = talib.MACD(prices['close'].values, self.short_period, self.long_period, self.smooth_period)
        # mydif, mydea, mybar = self.myMACD(prices['close'].values)
        prices["5d"] = prices["close"].rolling(window=5).mean()  # 周线
        prices["10d"] = prices["close"].rolling(window=10).mean()  # 半月线
        prices["20d"] = prices["close"].rolling(window=20).mean()  # 月线
        prices["60d"] = prices["close"].rolling(window=60).mean()  # 季度线
        prices[["close", "5d", "10d", "20d", "60d", ]].plot(figsize=(20, 10), grid=True)
        # plt.show()

        data_list = []
        for index, row in prices.iterrows():
            # 将时间转换为数字
            date_time = datetime.datetime.strptime(row['time_key'], '%Y-%m-%d %H:%M:%S')
            t = date2num(date_time)
            open = row['open']
            high = row['high']
            low = row['low']
            close = row['close']
            datas = (t, open, high, low, close)
            data_list.append(datas)

        # 创建子图
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        # 设置X轴刻度为日期时间
        ax.xaxis_date()
        plt.xticks(rotation=45)
        plt.yticks()
        plt.title("股票代码：00700")
        plt.xlabel("时间")
        plt.ylabel("股价（元）")
        mpf.candlestick_ohlc(ax, data_list, width=1.5, colorup='r', colordown='green')
        plt.grid()
        # fig = plt.figure(figsize=[18, 5])
        # plt.plot(df.index, macd, label='macd dif')
        # plt.plot(df.index, signal, label='signal dea')
        # plt.plot(df.index, hist, label='hist bar')
        # plt.plot(df.index, mydif, label='my dif')
        # plt.plot(df.index, mydea, label='my dea')
        # plt.plot(df.index, mybar, label='my bar')
        # plt.legend(loc='best')


if __name__ == "__main__":
    SHORT_PERIOD = 12
    LONG_PERIOD = 26
    SMOOTH_PERIOD = 9
    OBSERVATION = 100

    STOCK = "HK.00700"

    test = MACD(STOCK, SHORT_PERIOD, LONG_PERIOD, SMOOTH_PERIOD, OBSERVATION)
    test.handle_data()
