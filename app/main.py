import dash

from dash.dependencies import Input, Output
from dash import html, dcc
import plotly.graph_objs as go
import plotly.graph_objects as go

from dash import dash_table
from db.read import Read
from visualization.data_table import TimeDataTable
from visualization.ml import ML
from visualization.sleep import TimeSeriesPlot

max_length = 10

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)


def generate_section_banner(title):
    """ 패널 layout 부제목 """
    return html.Div(className="section-banner", children=title)


def build_banner():
    """ 배너 """
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Capstone Design of Soonchunhyang University"),
                    html.H6("Sleep Prediction Service"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
                        href="#",
                    ),
                ],
            ),
        ],
    )


def build_tabs():
    """ 메인 탭 """
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Member information",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    )
                ],
            ),

            # 탭 선택 화면
            html.Div(id='tabs-content')
        ],
    )


def build_quick_stats_panel1():
    """ member information 패널 왼쪽 기둥 탭 """
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Filter"),

                    # user input
                    html.Span("User ID Input",
                              style={"padding-bottom": "10px"}
                    ),
                    dcc.Input(id="user-input", type="text", placeholder="User ID", debounce=True,
                              value="9PCR7Y"),

                    # date input
                    html.Span("Date",
                              style={"padding": "10px"}
                     ),
                    dcc.Input(id="date-input", type="text", placeholder="2022-05-01", debounce=True,
                              value="2022-05-06"),

                    #
                    html.Span(id="user-output", style={"padding-top": "40px"}),
                    html.Span(id="date-output", style={"padding-top": "10px"}),
                ],
            )
        ],
    )


def build_bottom_panel1():
    """ tab 왼쪽 아래부분 """
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            # Metrics summary
            html.Div(
                className="eight columns",
                children=[
                    generate_section_banner("Sleep Time Series"),
                    html.Div(id="week-data-table")
                ],
            ),
            # Piechart
            html.Div(
                className="four columns",
                children=[
                    generate_section_banner("Predict Sleep Score"),
                    dcc.Graph(id="sleep-score-predict",
                              style={"height": "300px"})
                ],
            ),
        ],
    )


def build_top_panel1():
    """ tab 위부분 """
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Sleep Time Series"),

                    # 시각화 자료
                    dcc.Graph(id="sleep-time-serise",
                              style={"height": "88%"}),
                ],
            ),
            # Piechart
            html.Div(
                id="ooc-piechart-outer",
                className="four columns",
                children=[
                    generate_section_banner("Sleep Score"),

                    dcc.Graph(id="sleep-score",
                              style={"height": "88%"})
                ],
            ),
        ],
    )


app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),

        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
    ],
)


def no_data_plot():
    """ 데이터 없는 시각화 """
    return {
        "layout": {
            "xaxis": {
                "visible": False
            },
            "yaxis": {
                "visible": False
            },
            "annotations": [
                {
                    "text": "Data Not Found",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        }
    }


@app.callback(
    Output('week-data-table', 'children'),
    Input("user-input", "value"),
    Input("date-input", "value")
)
def week_date_table(user_input, date_input):
    """ 선택 날짜의 +- 3일 데이터 """
    dic_data = Read.origin_week_data(user_id=user_input, date=date_input)
    df = TimeDataTable.week_data_table(dic_data)
    return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i}
                 for i in df.columns],
        data=df.to_dict('records'),
        fixed_rows={'headers': True},
        style_cell={
            'minWidth': 95,
            'width': 95,
            'maxWidth': 95,
            'backgroundColor': 'rgb(255,255,255)',
            'color': 'rgb(22, 26, 40)'
        },
        style_table={'height': 300}  # default is 500
    )


@app.callback(
    Output("sleep-score", "figure"),
    Input("user-input", "value"),
    Input("date-input", "value")
)
def sleep_score_plot(user_input, date_input):
    """ 수면 스코어 시각화 """
    value = Read.sleep_score(user_id=user_input, date=date_input)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sleep Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))
    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})

    return fig


@app.callback(
    Output("sleep-score-predict", "figure"),
    Input("user-input", "value")
)
def sleep_predict_score_plot(user_input):
    """ 수면 스코어 시각화 """
    data = Read.ml_data(user_id=user_input)
    if len(data) > 5:
        value = ML.predict_score(data)
    else:
        value = 0

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sleep Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "skyblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100}}))
    fig.update_layout(paper_bgcolor="lavender", font={'color': "darkblue", 'family': "Arial"})

    return fig


# ------------------------------------ callback 함수 -------------------------------------------- #
@app.callback(
    Output('tabs-content', 'children'),
    Input('app-tabs', 'value')
)
def render_content(tab):
    """ 탭 선택 """
    if tab == 'tab1':
        return html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel1(),
                html.Div(
                    id="graphs-container",
                    children=[
                        build_top_panel1(),
                        build_bottom_panel1()
                    ],
                ),
            ]
        )


@app.callback(
    Output("user-output", "children"),
    Input("user-input", "value")
)
def user_input(input_id):
    return f'User ID : {input_id}'


@app.callback(
    Output("date-output", "children"),
    Input("date-input", "value")
)
def user_input(input_date):
    return f'Date : {input_date}'


@app.callback(
    Output("sleep-time-serise", "figure"),
    Input("user-input", "value"),
    Input("date-input", "value")
)
def display_sleep_time_series(user_input, date_input):
    data = Read.origin_data(user_id=user_input, date=date_input)
    if data:
        return TimeSeriesPlot.sleep_plot(data)
    else:
        return no_data_plot()


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)