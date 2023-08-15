import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from dash import Dash, dcc, html, Input, Output
import socket

HOST = socket.gethostbyname(socket.gethostname())
SEED = 20230620

sample_list = os.listdir('../samples')

def diff_data(data:pd.DataFrame) -> pd.DataFrame:
    '''
    Filters and creates the necessary variables for doing the outlier detection analysis.
    ------------------------------------------------------------------------------

    '''
    data['d_kert_reg'] = data['kert'] - data['kert'].shift(1)
    data['d_kert_forw'] = data['kert'] - data['kert'].shift(-1)
    return data

def median_ratio_outlier(data, col, r:float) -> pd.DataFrame:
    '''
    Defines outliers as the ratio to the median.
    ------------------------------------------
    '''
    ratio_outlier = (data[col]/np.nanmedian(data[col]) > r)
    return ratio_outlier

def diff_med_outlier(data:pd.DataFrame, med_col:str, diff:str, frwd_diff:str,  p:float, q:float) -> pd.DataFrame:
    '''
    Defines outliers based on the before and after difference of the values of interest and their comparison to the median.
    -----------------------------------------
    '''
    diff_outlier = (data[diff] >= p*np.nanmedian(data[med_col])) & (data[frwd_diff] >= q*np.nanmedian(data[med_col]))
    return diff_outlier

def ARIMA_outlier(data:pd.DataFrame, col:str, p:int, q:int, r:int, alpha:float) -> pd.DataFrame:
    '''
    Fits and arima(p,q,r) and gets confidence intervals for alpha for the fitted period. Deciding based on whether the actual observations is in the confidence interval or not. It is a one sided check as we are only interested in the upward tending outliers.
    -------------------------------------------------
    '''
    ar_model = ARIMA(data[col], order=(p,q,r))
    ar = ar_model.fit()
    prediction = ar.get_prediction()
    conf_int = prediction.conf_int(alpha=alpha)
    arima_outlier = (data[col] > conf_int.iloc[:,1])
    return arima_outlier

def iforest_outlier(data:pd.DataFrame, col:str, contamination:float) -> pd.DataFrame: 
    '''
    Fits an isolation forest to identify outliers in the time series.
    -------------------------------------------
    '''
    iforest_pred = IsolationForest(random_state=SEED, 
                                   bootstrap=True, 
                                   contamination=contamination
                                   ).fit_predict(data[[col]])
    forest_outlier = (iforest_pred == -1)
    return forest_outlier

def lof_outlier(data:pd.DataFrame, col:str, neighbors:int, contamination:float) -> pd.DataFrame: 
    '''
    Fits a local outlier factor model to identify outliers in the time series.
    -------------------------------------------
    '''
    lof_pred = LocalOutlierFactor(n_neighbors=neighbors,
                                      contamination=contamination
                                   ).fit_predict(data[[col]])
    lof_outlier = (lof_pred == -1)
    return lof_outlier




external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css?family=Lato"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Outlierek NRK5"


app.layout = html.Div(
    children=[
        # Header definition
        html.Div(
            children=[
                html.H1(
                    children="Nem rendszeres kereset és az 5 fő alattiak",          
                    className="header-title"
                    ),
                html.P(
                    children=(
                        "A projekt célja, hogy kiszűrjük az outliereket az 5 fő alatti vállalatok kifizetéseiből. "
                        "A weboldal egy interaktív outlier kereső az 5 fő alatti cégek bevallásai alapján."
                        ),
                    className="header-description",
                    ),
                ],
            className="header",
            ),
        # Menu definitions
        html.Div(
            children=[
                # File filter
                html.Div(
                    children=[
                        html.Div(children="file", className="menu-title"),
                        dcc.Dropdown(
                            id="file-filter",
                            options=[{"label": file, "value": file} for file in sample_list],
                            value = sample_list[0],
                            clearable=True,
                            className="dropdown",
                            ),
                        ]
                    ),

                # Code filter
                html.Div(
                    children=[
                        html.Div(children="code", className="menu-title"),
                        dcc.Dropdown(
                            id="code-filter",
                            placeholder = "Select an Option",
                            clearable=True,
                            className="dropdown",
                            ),
                        ]
                    ),

                # Outlier filter
                html.Div(
                    children=[
                        html.Div(children="outlier", className="menu-title"),
                        dcc.Dropdown(
                            id="outlier-filter",
                            placeholder = "Select an Option",
                            options = [{"label": "outlier_"+str(i), "value": "outlier_"+str(i)} for i in range(1,6)],
                            value = 'outlier_1', 
                            clearable=True,
                            className="dropdown",
                            ),
                        ]
                    ),

                # Date filter
                html.Div(
                    children=[
                        html.Div(children="Date Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date-range",
                            ),
                        ]
                    ),
                ],
            className="menu",
            ),
        

        # Graph definitions 
        html.Div(
            children=[
                # Level chart
                html.Div(
                    children=dcc.Graph(
                        id="level-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                # differenced chart
                html.Div(
                    children=dcc.Graph(
                        id="diff-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className='wrapper',
        ),
        ]
    )

@app.callback(
    Output("code-filter", "options"),
    Output("code-filter", "value"),
    Input("file-filter", "value"),
)
def update_dropdown(file):
    sample = pd.read_csv('../samples/'+file, usecols=range(1,7)) 
    codes = sample.code.unique()

    code_list = []

    for i in range(0, len(codes)):
        code_list.append({"label": codes[i], "value": codes[i]})

    return code_list, code_list[0]['value']

@app.callback(
        Output("date-range", "min_date_allowed"),
        Output("date-range", "max_date_allowed"),
        Output("date-range","start_date"),
        Output("date-range","end_date"),
        Input("file-filter", "value"), 
        Input("code-filter", "value")
)
def update_range(file, code):
    sample = pd.read_csv('../samples/'+file, usecols=range(1,7))
    sample = sample[sample['code'] == code]
    sample = sample[np.isnan(sample['kert']) == False]
    min_date_allowed=sample['date'].min()
    max_date_allowed=sample['date'].max()
    start_date=sample['date'].min()
    end_date=sample['date'].max()

    return min_date_allowed, max_date_allowed, start_date, end_date
    
@app.callback(
    Output("level-chart", "figure"),
    Output("diff-chart", "figure"),
    Input("file-filter", "value"), 
    Input("code-filter", "value"),
    Input("outlier-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_charts(file, code, outlier,  start_date, end_date):
    #Intialize analysis ts
    sample = pd.read_csv("../samples/"+file, usecols=range(1,7))
    sample['date'] = pd.to_datetime(sample['date'], format='%Y-%m-%d')
    filtered_data = sample[(sample['code']==code) & (sample['date'].between(start_date,end_date, inclusive='both'))]
    filtered_data = filtered_data[np.isnan(filtered_data['kert']) == False]
    filtered_data = diff_data(filtered_data)

    #Add outliers
    ##### Median based definitions
    filtered_data['outlier_1'] = median_ratio_outlier(filtered_data, 'kert', 1.5)
    #itt fontos, hogy mi a határidő amire meg kell mondani, hogy outlier-e? éven belül vagy havonta?
    filtered_data['outlier_2'] = diff_med_outlier(filtered_data, 'kert', 'd_kert_reg', 'd_kert_forw', 0.25, 0.2)
    ##### ARIMA based outlier
    filtered_data['outlier_3'] = ARIMA_outlier(filtered_data,'kert',0,0,1,0.1)
    ##### Machine learning based stuff
    ####### Isolation forest
    filtered_data['outlier_4'] = iforest_outlier(filtered_data,'kert',0.2)
    ###### Local outlier factor
    filtered_data['outlier_5'] = lof_outlier(filtered_data, 'kert', 10, 0.2)
    

    #Getting descriptive variable values for writing out
    tevcsop = filtered_data.loc[filtered_data.index[-1],'tevcsop']
    tevcsop = tevcsop.split('_')[1]
    szektor = filtered_data.loc[filtered_data.index[-1],'szektor']
    szektor = szektor.split('_')[1]
    ltszkat = filtered_data.loc[filtered_data.index[-1],'ltszkat']
    ltszkat = ltszkat.split('_')[1]

    level = [
        go.Scatter(
            x = filtered_data['date'],
            y = filtered_data['kert'],
            mode='lines',
            name='timeseries',
            hovertemplate = "%{x} : %{y:.2f} Ft<extra></extra>"
        ),
        go.Scatter(
            x = filtered_data.loc[filtered_data[outlier]==True, 'date'],
            y = filtered_data.loc[filtered_data[outlier]==True,'kert'],
            mode = 'markers',
            marker=dict(color="red", size=10, opacity=0.5),
            name = 'outlier',
            hovertemplate = "%{x} : %{y:.2f} Ft<extra></extra>"
        )
    ]

    diff = [
        go.Scatter(
            x = filtered_data['date'],
            y = filtered_data['d_kert_reg'],
            mode='lines',
            name='timeseries',
            hovertemplate = "%{x} : %{y:.2f} Ft<extra></extra>" 
        )
    ]


    level_chart_figure = go.Figure(data = level)
    level_chart_figure.update_layout(
        title={
            "text": f"Keresettömeg idősor: {code} <br> tevcsop: {tevcsop}, szektor: {szektor}, letszam: {ltszkat}, outlier: {outlier}",
            "x": 0.05,
            "xanchor": "left",
            },
        xaxis={"fixedrange": True},
        yaxis={"tickprefix": " Ft", "fixedrange": True},
        font = dict(
            size = 14
            ),
        showlegend = False,
        hoverlabel = dict(
            font_size = 14,
            font_family = "Rockwell"
        ),
        colorway=("#17B897",'red')
        )

    diff_chart_figure = go.Figure(data = diff)
    diff_chart_figure.update_layout(
        title={
            "text": f"Differenciált keresettömeg",
            "x": 0.05,
            "xanchor": "left",
            },
        xaxis={"fixedrange": True},
        yaxis={"tickprefix": " Ft", "fixedrange": True},
        font = dict(
            size = 14
            ),
        showlegend = False,
        hoverlabel = dict(
            font_size = 14,
            font_family = "Rockwell"
        ),
        colorway=["#E12D39"]
        )
    
    return level_chart_figure, diff_chart_figure

if __name__ == "__main__":
    app.run_server(debug=True, host=HOST, port=1234)