from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px


class TimeSeriesPlot:
    """ 시계열 데이터 """

    @staticmethod
    def sleep_plot(data):
        """ 하루 수면 시각화 """

        # 전처리
        df_data_list = []

        dict_list = data["data"]["levels"]["data"]
        for i in range(len(dict_list)):
            date = dict_list[i]["dateTime"].replace("T", " ")

            # row data
            df_data_list.append(
                {
                    "dateTime": datetime.fromisoformat(date),
                    "level": dict_list[i]["level"]
                }
            )
            df_data_list.append(
                {
                    "dateTime": datetime.fromisoformat(date)
                                + timedelta(seconds=dict_list[i]["seconds"]),
                    "level": dict_list[i]["level"]
                }
            )

        df = pd.DataFrame.from_dict(df_data_list)
        # 시각화
        fig = px.line(df, x="dateTime", y="level")

        # y 축 순서 변경
        fig.update_yaxes(categoryarray=["deep", "light", "rem", "wake"],
                         categoryorder="array")
        return fig