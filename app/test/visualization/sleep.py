import unittest

from db.read import Read
from visualization.sleep import TimeSeriesPlot

class TestTimeSeriesPlot(unittest.TestCase):

    def test_data_preprocessing(self):
        data = Read.origin_data(user_id="9PCR7Y", date="2022-05-06")
        TimeSeriesPlot.sleep_plot(data)