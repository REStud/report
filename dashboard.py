from dash import Dash, dcc, html, Input, Output
import socket
import processing
import slider_dates

HOST = socket.gethostbyname(socket.gethostname())
SEED = 20230620



external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css?family=Lato"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "REStud replication performance"


app.layout = html.Div(
    children=[
        # Header definition
        html.Div(
            children=[
                html.H1(
                    children="REStud replication team performance",          
                    className="header-title"
                    ),
                ],
            className="header",
            ),
        # Menu definitions
        html.Div(
            children=[
                html.Div(children='Time range', className='menu-title'),
                html.Div(
                    dcc.RangeSlider(
                        min=slider_dates.unix_time('2019-01-01'), 
                        max=slider_dates.unix_time('2023-09-05'),
                        value=[
                            slider_dates.unix_time('2019-01-01'),
                            slider_dates.unix_time('2023-09-05')
                            ],
                        id='time-filter',
                        marks=slider_dates.create_marks(
                                                start='2019-01-01',
                                                end='2023-09-05',
                                                n=26
                                                        )
                    ),
                    className="card"
                )
            ]
        ),
        # Graph definitions 
        html.Div(
            children=[
                # revision chart
                html.Div(
                    children=dcc.Graph(
                        id="revision-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                # differenced chart
                html.Div(
                    children=dcc.Graph(
                        id="time-at-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="main-issues",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="download-histograms",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="downloads",
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
    Output("revision-chart", "figure"),
    Output("time-at-chart", "figure"),
    Output("main-issues", "figure"),
    Output("download-histograms", "figure"),
    Output("downloads", "figure"),
    Input("time-filter","value") # here i have to create some interactive thingy
)
def create_charts(time_filter):
    git_data = processing.create_collapsed_git_data('data/git-events.dta')
    issues_data = processing.create_main_issues_data('data/issues.dta')
    zenodo_data = processing.create_zenodo_data('zenodo/zenodo_data_2022.csv','zenodo/zenodo_data_2021.csv')
    
    revision_chart = processing.revisions_chart(git_data)
    time_at_chart = processing.time_at_editor_chart(git_data)
    main_issues_chart = processing.main_issues_chart(issues_data)
    download_histograms_chart = processing.downloads_per_month_chart(zenodo_data)
    downloads_chart = processing.downloads_chart(zenodo_data)

    return revision_chart, time_at_chart, main_issues_chart, download_histograms_chart, downloads_chart

if __name__ == "__main__":
    app.run_server(debug=True, host=HOST, port=1234)