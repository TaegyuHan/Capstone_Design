import json
import pathlib
import os
from key import MONGODB_CONNECTION_STRING
import pymongo as pymongo


class DataTransformation:
    """ 데이터 변형 """

    def __init__(self) -> None:
        """ 생성자 """
        self._current_path = os.path.dirname(os.path.abspath(__file__))
        self._json_path = f"{self._current_path}/json"

    def _read_json(self, file_path: str) -> dict:
        """ json 파일 읽기 """
        with open(file_path) as json_file:
            data = json.load(json_file)
        return data

    def json_data_check(self) -> bool:
        """ json 데이터 확인하기 """
        if len(list(pathlib.Path(self._json_path).glob('*.json'))):
            return True
        return False

    def read_json_all(self) -> dict:
        """ json 파일 읽어서 dict 형식으로 반환하기

        :return: dict type json 데이터
        """
        json_files = list(pathlib.Path(self._json_path).glob('*.json'))

        if not json_files:
            raise "json 폴더에 json 파일이 존재하지 않습니다."

        for file_path in json_files:
            dict_json = self._read_json(file_path)
            yield dict_json


class InsertMongoDB:
    """ mongodb에 데이터 넣기 """

    def __init__(self):
        """ 생성자 """
        self._DT = DataTransformation()

    def original_data_insert_db(self) -> None:
        """ api원본 데이터 db에 sleep 데이터 넣기 """

        with pymongo.MongoClient(MONGODB_CONNECTION_STRING) as client:
            db = client.CapstoneProject
            collection_currency = db.ModelSleepLogByDate

            for user_id_date_range_data in self._DT.read_json_all():
                user_id = user_id_date_range_data["userId"]
                data = user_id_date_range_data["data"]["sleep"]

                for row_data in data:
                    date = row_data["dateOfSleep"]
                    del row_data["dateOfSleep"]

                    json_row = {
                        "userId": user_id,
                        "date": date,
                        "data":row_data
                    }

                    # 데이터 넣기
                    collection_currency.insert_one(json_row)


if __name__ == '__main__':
    IMD = InsertMongoDB()
    IMD.original_data_insert_db()
