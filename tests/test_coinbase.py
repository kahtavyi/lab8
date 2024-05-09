from dataloader.coinbaseloader import CoinbaseLoader
import json
import pytest
import pandas as pd
from dataloader.coinbaseloader import Granularity
from datetime import datetime

input_data = [
    {"id": 1, "name": "BTC", "price": 50000},
    {"id": 2, "name": "ETH", "price": 2500},
    {"id": 3, "name": "SOL", "price": 200}
]

class TestClass:

    def test_get_pairs(self):
        loader = CoinbaseLoader()
        data = loader.get_pairs()
        assert data is not None and len(data) != 0, "Empty pairs list received"
        assert isinstance(data, pd.DataFrame), "Pandas DataFrame expected"
        assert "BTC" in data.base_currency.values, "BTC base currency not found"

    @pytest.mark.parametrize("input_data", input_data)
    def test_get_stats(self, input_data):
        json_data = json.dumps(input_data)
        assert json_data is not None
        assert isinstance(json_data, str)
        parsed_data = json.loads(json_data)
        assert parsed_data == input_data


    @pytest.fixture
    def coinbase_loader(self):
        return CoinbaseLoader()

    @pytest.mark.parametrize("pair, begin, end, granularity", [
    ("BTC-USD", datetime(2023, 1, 1), datetime(2023, 1, 2), Granularity.ONE_HOUR),
    ("ETH-USD", datetime(2022, 10, 1), datetime(2022, 10, 2), Granularity.SIX_HOURS),
    ("SOL-USD", datetime(2022, 12, 1), datetime(2022, 12, 2), Granularity.ONE_DAY)
])
    def test_get_historical_data(self, coinbase_loader, pair, begin, end, granularity):
        historical_data = coinbase_loader.get_historical_data(pair, begin, end, granularity)
        json_data = historical_data.to_json(orient="records")
        assert json_data is not None
        assert isinstance(json_data, str)

        
        actual_columns = historical_data.columns.tolist()
        expected_columns = ['low', 'high', 'open', 'close', 'volume']

        assert actual_columns == expected_columns
     
    
    

    
