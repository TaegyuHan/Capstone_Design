import unittest

from db.read import Read


class TestSelect(unittest.TestCase):

    def test_origin_data(self):
        Read.origin_data(user_id="9PCR7Y", date="2022-05-06")

    def test_ml_data(self):
        """ 모델 데이터 테스트 """
        Read.ml_data(user_id="9PCR7Y")
