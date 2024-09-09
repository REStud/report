from dash import Dash, dcc, html, Input, Output
import socket
import processing
import pandas as pd

HOST = socket.gethostbyname('localhost')
SEED = 20230620
TABLE_DICT = {'total_time':'total_time', 'time_at_author':'time_at_author', 'time_at_editor':'time_at_editor'}

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
                    children="Date Editor's Report 2024",          
                    className="header-title"
                    ),
                ],
            className="header",
            ),
        # Graph definitions 
        html.Div(
            children=[
                dcc.Markdown('''
                This report covers the period between September 1, 2022 and August 31, 2024. In this period, xx replication packages have been submitted and xx packages have been accepted. 

                We now have four complete years of data under the new Data Availability Policy. This makes it possible to make comparisons and identify changes.
                             
                ## Turnaround times

                The vast majority of packages are accepted only after revisions; only XXX packages were accepted as submitted. Most packages are accepted on first revision. The Figure plots the number of packages by revisions at the time acceptance. Around 58 percent of packages are accepted after at most one revision (up from 52 percent last year).
                '''),
                # revision chart
                html.Div(
                    children=dcc.Graph(
                        id="revision-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                dcc.Markdown('''
                Some comparison how the team efficiency is changing by years....
                '''),
                # revision year chart
                html.Div(
                    children=dcc.Graph(
                        id="revision-year-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                dcc.Markdown('''
                The average package accepted this year received their first response from the Data Editor in xx days (up from xx days last year). This statistic excludes papers where the Data Availability Policy does not apply. For revisions, the mean response time is x days, with the majority of packages decided in much shorter time (see Figure).
                '''),
                # time at editor chart
                html.Div(
                    children=dcc.Graph(
                        id="time-at-chart",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                dcc.Markdown('''
                The average time authors spend with a revision is XX days.

                ## Reasons for revision

                The Figure shows the main reasons for sending back the first version of the package for revision. About half of the packages miss data citations, a Data Availability Statement, or both. About a third of the packages do not save or include the reproducible exhibits to be verified. Specific Stata requirements are also often inadequately explained. 
                '''),
                
                # main issues chart
                html.Div(
                    children=dcc.Graph(
                        id="main-issues",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                dcc.Markdown('''
                ## Impact

                The median replication package is downloaded from Zenodo x times a month. This includes views and downloads by author and editorial team. As the figure shows, there is substantial heterogeneity across packages in their download statistics, but all packages have some visibility.
                '''),
                # download histograms
                html.Div(
                    children=dcc.Graph(
                        id="download-histograms",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                dcc.Markdown('''
                Download statistics are highly correlated over time. Packages that were popular last year are often downloaded also this year (next Figure). This suggests that the download statistics capture genuine interest and not only driven by early downloads by authors and the editorial team. 
                '''),
                # download scatter chart
                html.Div(
                    children=dcc.Graph(
                        id="downloads",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                html.Br(),
                
                # table filter
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="table", className="menu-title"),
                                dcc.Dropdown(
                                    id="table-filter",
                                    options=TABLE_DICT,
                                    value = TABLE_DICT['total_time'],
                                    clearable=True,
                                    className="dropdown",
                                    ),
                                ]
                            ),
                    ], 
                    className='menu'
                ),
                html.Br(),
                html.Br(),
                # top table chart
                dcc.Markdown('''
                Here should be some information on the tables....
                '''),
                html.Div(
                    children=dcc.Graph(
                        id="top-table",
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
    Output("revision-year-chart", "figure"),
    Output("time-at-chart", "figure"),
    Output("main-issues", "figure"),
    Output("download-histograms", "figure"),
    Output("downloads", "figure"),
    Output("top-table", "figure"),
    Input("table-filter","value") # here i have to create some interactive thingy
)
def create_charts(table):
    collapsed = pd.read_stata('temp/collapsed_accepted_at.dta')
    revisions = processing.create_revisions_year_data('temp/collapsed_year.dta')
    issues_data = processing.create_main_issues_data('data/issues.dta', 'temp/git-events-processed.dta')
    zenodo_data = pd.read_stata('temp/zenodo.dta')
    time_table = processing.create_time_tables('temp/collapsed_year.dta')
    
    revision_chart = processing.revisions_chart(collapsed)
    revision_year_chart = processing.revisions_year_chart(revisions)
    time_at_chart = processing.time_at_editor_chart(collapsed)
    main_issues_chart = processing.main_issues_chart(issues_data)
    download_histograms_chart = processing.downloads_per_month_chart(zenodo_data)
    downloads_chart = processing.downloads_chart(zenodo_data)
    top_table_chart = processing.top_table(time_table, table)

    return revision_chart, revision_year_chart, time_at_chart, main_issues_chart, download_histograms_chart, downloads_chart, top_table_chart

if __name__ == "__main__":
    app.run_server(debug=True, host=HOST, port=4440)