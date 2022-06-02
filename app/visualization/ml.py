import pandas as pd
from sklearn.preprocessing import StandardScaler

from xgboost import XGBRegressor
from catboost import CatBoostRegressor

import lightgbm as LGB
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import (
    Ridge, Lasso, ElasticNet, LinearRegression
)
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import (
    train_test_split, KFold, cross_val_score
)
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

class ML:
    """ 시계열 데이터 """

    @staticmethod
    def rmse(y_pred, y):
        rmse = mean_squared_error(y, y_pred) ** 0.5
        return rmse

    @staticmethod
    def predict_score(data):
        """ 실행 """
        df_data_list = []

        for row in data:
            # josn 파싱
            df_data_list.append({
                "dateOfSleep": row["date"],
                "efficiency": row["data"]["efficiency"],
                "sleepstart": row["data"]["startTime"],
                "sleepend": row["data"]["endTime"],
                "minutesAfterWakeup": row["data"]["minutesAfterWakeup"],
                "minutesAsleep": row["data"]["minutesAsleep"],
                "minutesAwake": row["data"]["minutesAwake"],
                "timeInBed": row["data"]["timeInBed"],
                "minutesToFallAsleep": row["data"]["minutesToFallAsleep"],

                "deep_count": row["data"]["levels"]["summary"]["deep"]["count"],
                "deep_minutes": row["data"]["levels"]["summary"]["deep"]["minutes"],
                "deep_thirtyDayAvgMinutes": row["data"]["levels"]["summary"]["deep"]["thirtyDayAvgMinutes"],

                "wake_count": row["data"]["levels"]["summary"]["wake"]["count"],
                "wake_minutes": row["data"]["levels"]["summary"]["wake"]["minutes"],
                "wake_thirtyDayAvgMinutes": row["data"]["levels"]["summary"]["wake"]["thirtyDayAvgMinutes"],

                "rem_ count": row["data"]["levels"]["summary"]["rem"]["count"],
                "rem_ minutes": row["data"]["levels"]["summary"]["rem"]["minutes"],
                "rem_ thirtyDayAvgMinutes": row["data"]["levels"]["summary"]["rem"]["thirtyDayAvgMinutes"],

                "light_count": row["data"]["levels"]["summary"]["light"]["count"],
                "light_minutes": row["data"]["levels"]["summary"]["light"]["minutes"],
                "light_thirtyDayAvgMinutes": row["data"]["levels"]["summary"]["light"]["thirtyDayAvgMinutes"]
            })

        # df 만들기
        df = pd.DataFrame.from_dict(df_data_list)

        # sleepstart, sleepend는 제외
        df = df.iloc[:, 1:]
        df = df[df.columns.difference(['sleepstart', 'sleepend'])]

        # train, test 나누기
        X = df.iloc[:, 1:]
        Y = df.iloc[:, 3]


        x_train, x_val, y_train, y_val = train_test_split(X, Y,
                                                          test_size=0.2,
                                                          shuffle=True,
                                                          random_state=34)
        x_val, x_test, y_val, y_test = train_test_split(x_val, y_val,
                                                        test_size=0.5,
                                                        shuffle=True,
                                                        random_state=34)

        # 표준화
        sc = StandardScaler()
        x_train = sc.fit_transform(x_train)
        x_val = sc.fit_transform(x_val)
        x_test = sc.fit_transform(x_test)

        # 5 kfold cross validation
        kfold = KFold(n_splits=5, shuffle=True, random_state=0)

        # 모델
        models = []
        models.append(['Ridge', Ridge()])
        models.append(['Lasso', Lasso()])
        models.append(['ElasticNet', ElasticNet()])
        models.append(['SVR', SVR()])
        models.append(['Random Forest', RandomForestRegressor()])
        models.append(['XGBoost', XGBRegressor()])
        models.append(['LinearRegression', LinearRegression()])
        models.append(['CatBoostRegressor', CatBoostRegressor(logging_level=("Silent"))])
        models.append(['PLSRegression', PLSRegression()])
        models.append(['Lightgbm', LGB.LGBMRegressor()])


        list_1 = []
        min_score = []
        best_model = 0
        score = 0
        # 5회 교차검증
        for m in range(len(models)):
            model = models[m][1]
            scores = -1 * cross_val_score(model, x_train, y_train, cv=kfold,
                                          scoring="neg_mean_squared_error")  # 교차검증 MSE
            score = min(scores)
            list_1.append(scores)
            if len(min_score) > 1:
                if score < min(min_score):
                    best_model = model
            else:
                best_model = model
            min_score.append(score)

        df_1 = pd.DataFrame(models)
        df = pd.DataFrame(list_1)
        df.index = df_1.iloc[:, 0]

        best_model.fit(x_train, y_train)
        pred = best_model.predict(x_val)

        return pred[0]













