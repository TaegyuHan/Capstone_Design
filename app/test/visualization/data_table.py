import unittest

from db.read import Read
from visualization.data_table import TimeDataTable

class TestTimeDataTable(unittest.TestCase):

    def test_data_preprocessing(self):
        data = Read.origin_week_data(user_id="9PCR7Y", date="2022-05-06")
        TimeDataTable.week_data_table(data)