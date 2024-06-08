import pandas as pd
from datetime import datetime
from abc import abstractmethod

from binance.client import Client

import sys
sys.path.append('./')
from const import *   # import the const.


# log in
client = Client(BINANCE_ID, BINANCE_PASSWORD)


# functions
def transfer_timestamp(time):
    return datetime.fromtimestamp(time / 1000).strftime('%Y-%m-%d %H:%M:%S')

# datadownloader
## datadownloadere template
class DataDownloaderTemplate(object):
    """
    the template of datadownloader

    3 functions:
    1. obtain the data
    2. transfer the format of the data
    3. save the data
    """

    @abstractmethod
    def obtain_data(self, **parameters):
        """
        parameters: the parameters used to obtain the data from the data source
        """
        pass

    @abstractmethod
    def transfer_data(self, data):
        pass

    def save_data(self, data, file_name):
        data.to_csv(self.root_path + "/{}.csv".format(file_name))
        pass

    def download_data(self, file_name, **obtain_paramaters):
        """
        用于下载数据的对外接口
        """
        data = self.obtain_data(**obtain_paramaters)
        transfer_data = self.transfer_data(data)
        self.save_data(data=transfer_data, file_name=file_name)
    
    pass

## kline datadownloader
class KlineDataDownloader(DataDownloaderTemplate):
    """
    用于下载K线数据

    类参数：均为默认参数
    1. client类
    2. 数据存储根目录
    3. columns

    对外接口传入参数：
    1. symbol: 标的
    2. start_str: 开始日期
    3. end_date: 结束日期
    4. interval: 数据间隔，默认为1分钟
    """
    def __init__(self, root_path=DATA_ROOT_PATH_KLINE, columns=KLINE_COLUMNS, client=client) -> None:
        """
        root_path: 该类数据所在的根目录
        columns: dataframe的columns
        client: 登录binance后的类
        """
        self.root_path = root_path
        self.columns = columns
        self.client = client
        pass

    def obtain_data(self, symbol, start_str, end_str, interval=Client.KLINE_INTERVAL_1MINUTE):
        """"""
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, 
                                                   start_str=start_str, end_str=end_str)
        return klines
    
    def transfer_data(self, data):
        data = pd.DataFrame(data, columns=self.columns)
        
        for time_stamp in ["open_time", "close_time"]:
            data[time_stamp] = data[time_stamp].apply(lambda x: transfer_timestamp(x))

        for price_volume in ["open", "high", "low", "close", "volume", "amount", "call_volume", "call_amount"]:
            data[price_volume] = data[price_volume].astype(float)

        data["number"] = data["number"].astype(int)
        
        return data
    pass



DATA_ROOT_PATH_DAILYPRICE = "data/daily_price"

class DailyPriceDataDownloader(DataDownloaderTemplate):
    """
    用于下载日频量价（K线）数据

    类参数：均为默认参数
    1. client类
    2. 数据存储根目录
    3. columns

    对外接口传入参数：
    1. symbol: 标的
    2. start_str: 开始日期
    3. end_date: 结束日期
    4. interval: 数据间隔，默认为一天
    """
    def __init__(self, root_path=DATA_ROOT_PATH_DAILYPRICE, columns=KLINE_COLUMNS, client=client) -> None:
        """
        root_path: 该类数据所在的根目录
        columns: dataframe的columns
        client: 登录binance后的类
        """
        self.root_path = root_path
        self.columns = columns
        self.client = client
        pass

    def obtain_data(self, symbol, start_str, end_str, interval=Client.KLINE_INTERVAL_1DAY):
        """"""
        klines = self.client.get_historical_klines(symbol=symbol, interval=interval, 
                                                   start_str=start_str, end_str=end_str)
        return klines
    
    def transfer_data(self, data):
        data = pd.DataFrame(data, columns=self.columns)
        
        for time_stamp in ["open_time", "close_time"]:
            data[time_stamp] = data[time_stamp].apply(lambda x: transfer_timestamp(x))

        for price_volume in ["open", "high", "low", "close", "volume", "amount", "call_volume", "call_amount"]:
            data[price_volume] = data[price_volume].astype(float)

        data["number"] = data["number"].astype(int)
        
        return data
    pass
        