from datetime import datetime, timedelta
from key import MONGODB_CONNECTION_STRING
import pymongo as pymongo


class Read:
    """ 데이터 불러오기 """

    # 기존 유저와 date
    user_id = ""
    date = ""
    _origin_data = {}
    _score_data = 0
    _origin_week_data = []
    _ml_data = []

    @staticmethod
    def origin_data(user_id: str, date: str):
        """ 오리지널 데이터 데이터 """

        # DB 연동 설정
        if Read.user_id == user_id \
                and Read.date == date \
                and not Read._origin_data:
            return Read._origin_data

        with pymongo.MongoClient(MONGODB_CONNECTION_STRING) as client:
            db = client["CapstoneProject"]
            collection = db["ModelSleepLogByDate"]

            query = {
                "userId": user_id,
                "date": date
            }

            # 연동
            docs = collection.find(query)

            for doc in docs: # 주 수면 필터링
                if doc["data"]["isMainSleep"]:
                    Read._origin_data = doc
                    return doc

    @staticmethod
    def origin_week_data(user_id: str, date: str):
        """ 선택 날짜로 부터 앞뒤로 3일 추가 """

        week_date = []
        diff_day = 3 # 3일

        # DB 연동 설정
        if Read.user_id == user_id \
                and Read.date == date \
                and not Read._origin_week_data:
            return Read._origin_week_data

        # 날짜 계산하기
        today = datetime.strptime(date, "%Y-%m-%d")
        before = str((today - timedelta(days=diff_day)).date())
        after = str((today + timedelta(days=diff_day)).date())

        with pymongo.MongoClient(MONGODB_CONNECTION_STRING) as client:
            db = client["CapstoneProject"]
            collection = db["ModelSleepLogByDate"]

            query = {
                "userId": user_id,
                "date": {
                    "$gt": before,
                    "$lt": after
                }
            }

            # 연동
            docs = collection.find(query)

            for doc in docs: # 주 수면 필터링
                if not doc["data"]["isMainSleep"]:
                    continue
                week_date.append(doc)

        Read._origin_week_data = week_date
        return Read._origin_week_data


    @staticmethod
    def sleep_score(user_id: str, date: str) -> int:
        """ 오리지널 데이터 데이터 """

        # DB 연동 설정
        if Read.user_id == user_id and Read.date == date:
            return Read._score_data["data"]["efficiency"]

        with pymongo.MongoClient(MONGODB_CONNECTION_STRING) as client:
            db = client["CapstoneProject"]
            collection = db["ModelSleepLogByDate"]

            query = {
                "userId": user_id,
                "date": date
            }

            # 연동
            docs = collection.find(query)

            for doc in docs: # 주 수면 필터링
                if doc["data"]["isMainSleep"]:
                    Read._score_data = doc
                    return doc["data"]["efficiency"]

    @staticmethod
    def ml_data(user_id: str):
        """ 모델 input 데이터 가져오기 """
        ml_data = []

        # DB 연동 설정
        if Read.user_id == user_id:
            return Read._ml_data

        with pymongo.MongoClient(MONGODB_CONNECTION_STRING) as client:
            db = client["CapstoneProject"]
            collection = db["ModelSleepLogByDate"]

            query = {
                "userId": user_id
            }

            # 연동
            docs = collection.find(query)

            for doc in docs: # 주 수면 필터링
                if doc["data"]["isMainSleep"]:
                    ml_data.append(doc)

        Read._ml_data = ml_data
        return Read._ml_data


if __name__ == '__main__':
    Read.origin_week_data(user_id="9PCR7Y", date="2022-05-06")