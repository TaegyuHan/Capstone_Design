import json
import requests
from http import HTTPStatus
import key


class FitBitAPIRequestHandler:
    """ Fitbit 데이터 호출

        sleep API 호출
        URL : https://dev.fitbit.com/build/reference/web-api/sleep/get-sleep-log-by-date-range/
    """

    def __init__(self, start_date: str, end_date: str) -> None:
        """ 생성자 """
        self._START_DATE = start_date # "2022-05-24"
        self._END_DATE = end_date # "2022-05-30"
        self._keys = key.API_KEY

    def _URL(self, user_id: str) -> str:
        """ API 호출 URL 생성

        :param user_id: Fitbit API 유저 ID
        :return:API 호출 URL
        """

        return (
            f"https://api.fitbit.com/1.2/user/{user_id}/sleep/date/{self._START_DATE}/{self._END_DATE}.json"
        )

    def _sleep_api_requests(self, user_id: str) -> requests.Response:
        """ sleep api 호출하기

        :param user_id: Fitbit API 유저 ID
        :return: api 응답 코드
        """
        url = self._URL(user_id)
        token = self._keys[user_id]

        response = requests.get(
            url=url,
            headers={
                "accept": "application/json",
                "authorization": f"Bearer {token}"
            }
        )
        return response

    def sleep_api_requests_all_save(self) -> None:
        """ sleep api json으로 저장하기

            저장 경로 PATH : api/data/json

        :return: None
        """
        for user_id, _ in self._keys.items():
            response = self._sleep_api_requests(user_id)

            if response.status_code != HTTPStatus.OK:
                continue # HTTP 응답 실패 pass

            # json 파일 저장하기
            with open((f'./data/json/{user_id}_sleep_data_'
                       f'{self._START_DATE}_{self._END_DATE}.json'), 'w') as outfile:

                json_data = {
                    "userId": user_id,
                    "data": response.json()
                }
                json.dump(json_data, outfile)


if __name__ == '__main__':
    API = FitBitAPIRequestHandler()
    API.sleep_api_requests_all_save()
    # DT = data.DataTransformation()
    pass



