import pandas as pd


class TimeDataTable:
    """ 시계열 데이터 """

    @staticmethod
    def week_data_table(data: str):
        """ 일주일 데이터 테이블

            입력 받은 날짜의 +3일 -3일이 들어갑니다.
            +3일이 존재 하지 않으면 존재 하지 않는 만큼 -로 들어갑니다.

        :param date: 날짜
        :return:
        """
        df_data_list = []

        for row in data:
            df_data_list.append({

                "user_id": row["userId"],
                "date": row["date"],
                "duration": row["data"]["duration"],
                "efficiency": row["data"]["efficiency"],
                "start_time": row["data"]["startTime"],
                "end_time": row["data"]["endTime"],

                "deep_count": row["data"]["levels"]["summary"]["deep"]["count"],
                "deep_minutes": row["data"]["levels"]["summary"]["deep"]["minutes"],

                "light_count": row["data"]["levels"]["summary"]["light"]["count"],
                "light_minutes": row["data"]["levels"]["summary"]["light"]["minutes"],

                "rem_count": row["data"]["levels"]["summary"]["rem"]["count"],
                "rem_minutes": row["data"]["levels"]["summary"]["rem"]["minutes"],

                "wake_count": row["data"]["levels"]["summary"]["wake"]["count"],
                "wake_minutes": row["data"]["levels"]["summary"]["wake"]["minutes"]
            })

        df_data_list.reverse()
        df = pd.DataFrame.from_dict(df_data_list)

        return df