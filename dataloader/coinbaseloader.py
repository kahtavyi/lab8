import json
import pandas as pd
from datetime import datetime
from pandas.core.api import DataFrame as DataFrame
from dataloader.baseloader import BaseDataLoader
from dataloader.baseloader import BaseDataLoader
from enum import Enum
import mplfinance as mpf

import logging

class Granularity(Enum):
    ONE_MINUTE=60,
    FIVE_MINUTES=300,
    FIFTEEN_MINUTES=900,
    ONE_HOUR=3600,
    SIX_HOURS=21600,
    ONE_DAY=86400

class CoinbaseLoader(BaseDataLoader):

    def __init__(self, endpoint="https://api.exchange.coinbase.com"):
        super().__init__(endpoint)
        self._logger = logging.getLogger("COINBASE")
        self._logger.info("succesfully logged")

    def get_pairs(self) -> pd.DataFrame:
        self._logger.debug("get pairs")
        data = self._get_req("/products")
        df = pd.DataFrame(json.loads(data))
        df.set_index('id', drop=True, inplace=True)
        return df

    def get_stats(self, pair: str) -> pd.DataFrame:
        self._logger.debug(f"get pair {pair} stats")
        data = self._get_req(f"/products/{pair}")
        return pd.DataFrame(json.loads(data), index=[0])

    def get_historical_data(self, pair: str, begin: datetime, end: datetime, granularity: Granularity) -> DataFrame:
        self._logger.debug(f"get pair {pair}")
        params = {
            "start": begin,
            "end": end,
            "granularity": granularity.value
        }

        data = self._get_req("/products/" + pair + "/candles", params)
        # parse response and create DataFrame from it
        df = pd.DataFrame(json.loads(data),
                          columns=("timestamp", "low", "high", "open", "close", "volume"))

        df.set_index('timestamp', drop=True, inplace=True)

        df.index = pd.to_datetime(df.index)
        return df

def calculate_rsa(data, window):
    return data['close'].rolling(window).mean() / data['close'].rolling(window).std()

if __name__ == "__main__":
    loader = CoinbaseLoader()
    