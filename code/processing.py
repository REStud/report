import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

def create_collapsed_git_data(path:str) -> pd.DataFrame: 
    '''
    
    '''
    analysis_df = pd.read_stata(path)
    analysis_df = analysis_df.sort_values(by=['MS', 'numeric_date'])
    analysis_df['spell'] = (analysis_df['numeric_date']-analysis_df['numeric_date'].shift(1))/3600/24
    analysis_df['matching'] = (analysis_df['MS'] == analysis_df['MS'].shift(1))
    make_missing = analysis_df.index[analysis_df['matching']==False]
    analysis_df.loc[make_missing, 'spell'] = np.NaN
    analysis_df['at_editor'] = (analysis_df['branch_imputed'].shift(1) == analysis_df['branch_imputed']) | (analysis_df['branch_imputed'].shift(1) == 'author')
    analysis_df['change'] = -(analysis_df['at_editor'].shift(1)==analysis_df['at_editor'])
    analysis_df['spell_id'] = analysis_df.groupby('MS')['change'].transform(pd.Series.cumsum)

    collapsed = analysis_df.groupby(by=['MS', 'accepted_at', 'spell_id', 'at_editor']).sum().reset_index()
    collapsed = collapsed[['MS', 'accepted_at', 'spell_id', 'at_editor', 'spell']]
    collapsed = collapsed[collapsed['spell_id'] != 1]
    collapsed['spell_id'] = np.floor((collapsed['spell_id']-1)/2)
    collapsed['spell_id'] = collapsed['spell_id'].astype(int)
    collapsed = collapsed.pivot(index=['MS', 'spell_id'], columns='at_editor', values=['spell', 'accepted_at']).reset_index()
    collapsed.columns = ['MS', 'revision','time_at_author', 'time_at_editor', 'accepted_at0', 'accepted_at']
    collapsed.drop('accepted_at0',axis=1,inplace=True)
    collapsed['max_revision'] = collapsed.groupby('MS')['revision'].transform(pd.Series.max)

    return collapsed

def create_revisions_year_data(path:str) -> pd.DataFrame:
    '''
    
    '''
    collapsed_year = pd.read_stata(path)
    collapsed_year = collapsed_year[['MS', 'year', 'max_revision']]
    revisions = collapsed_year.groupby(['MS', 'year']).mean().reset_index()
    revisions['max_revision'] = revisions['max_revision'].apply(lambda x:int(x))
    revisions = revisions.groupby(['year','max_revision']).count().reset_index()
    years = revisions[['year','MS']].groupby('year').sum()
    revisions.loc[revisions['year']==2021,'percent'] = revisions.loc[revisions['year']==2021, 'MS']/years.loc[2021,'MS']
    revisions.loc[revisions['year']==2022,'percent'] = revisions.loc[revisions['year']==2022, 'MS']/years.loc[2022,'MS']
    revisions.loc[revisions['year']==2023,'percent'] = revisions.loc[revisions['year']==2023, 'MS']/years.loc[2023,'MS']
    revisions.loc[revisions['year']==2024,'percent'] = revisions.loc[revisions['year']==2024, 'MS']/years.loc[2024,'MS']

    return revisions

def create_time_tables(path:str) -> pd.DataFrame:
    '''
    
    '''
    collapsed_year = pd.read_stata(path)
    time_tables = collapsed_year.groupby('MS').sum()[['time_at_author','time_at_editor']]
    time_tables = time_tables.merge(collapsed_year[['MS','year']], how='left', on='MS')
    time_tables = time_tables.drop_duplicates(['MS','year'])
    time_tables = time_tables[time_tables['year']==2024]
    time_tables['total_time'] = time_tables['time_at_author'] + time_tables['time_at_editor']
    time_tables['total_time'] = time_tables['total_time'].apply(lambda x: round(x))
    time_tables['time_at_author'] = time_tables['time_at_author'].apply(lambda x: round(x))
    time_tables['time_at_editor'] = time_tables['time_at_editor'].apply(lambda x: round(x))

    return time_tables

def create_main_issues_data(issues:str, git_data:str) -> pd.DataFrame:
    '''
    
    '''
    issues_data = pd.read_stata(issues)
    ms = pd.read_stata(git_data)
    issues_data.drop_duplicates(['MS'],inplace=True)
    ms = ms[['MS']].drop_duplicates(['MS'])
    issues_data = ms.merge(issues_data,how='left',on='MS')
    issues_data.drop(['branch', 'commit'],axis=1,inplace=True)
    issues_data = issues_data.drop_duplicates(['MS'])
    issues_data.drop(['MS', 'macosx', 'forward_slash', 'relative_path', ],axis=1,inplace=True)

    mean_issues = dict()
    for col in issues_data.columns:
        mean_issues[col] = issues_data[col].mean()

    mean_issues = pd.DataFrame(mean_issues,index=[0]).melt()
    mean_issues.columns = ['issue', 'value']
    mean_issues['value'] = mean_issues['value'] * 100 
    mean_issues.sort_values('value',inplace=True, ascending=False, ignore_index=True)
    mean_issues.loc[0,'issue'] = "Cite data"
    mean_issues.loc[2,'issue'] = "Save output"
    mean_issues.loc[3,'issue'] = "Stata packages"
    mean_issues.loc[4,'issue'] = "Matlab toolboxes"
    mean_issues.loc[5,'issue'] = "Confidential Data"
    mean_issues.loc[6,'issue'] = "Include Data"
    mean_issues.loc[7,'issue'] = "Insufficient hardware doc"
    mean_issues.loc[8,'issue'] = "Insufficient sotfware doc"
    mean_issues.loc[9,'issue'] = "No/multiple readme(s)"
    mean_issues = mean_issues.sort_values('value').reset_index(drop=True)
    mean_issues.drop(0,inplace=True)
    mean_issues.reset_index(drop=True,inplace=True)

    return mean_issues

def manipulate_zenodo22(zenodo22:pd.DataFrame) -> pd.DataFrame:
    '''
    
    '''
    zenodo22['created_at'] = zenodo22['created'].apply(lambda x: datetime.strptime(x.split('T')[0],'%Y-%m-%d'))
    zenodo22.drop(['downloads', 'views', 'revision', 'created'], axis=1, inplace=True)
    zenodo22.columns = ['id', 'downloads', 'views', 'created_at']
    zenodo22['year'] = '2022'
    return zenodo22

def manipulate_zenodo21(zenodo21:pd.DataFrame) -> pd.DataFrame:
    '''
    
    '''
    zenodo21.drop(['downloads', 'views', 'revisions'], axis=1, inplace=True)
    zenodo21.columns = ['id', 'downloads', 'views']
    zenodo21['year'] = '2021'
    return zenodo21

def manipulate_merged_zenodo(zenodo:pd.DataFrame) -> pd.DataFrame:
    '''
    
    '''
    zenodo['starts_at'] = "2021-09-14"
    zenodo.loc[zenodo['year']=='2022','starts_at'] = "2022-09-07"
    zenodo['starts_at'] = zenodo['starts_at'].apply(lambda x : datetime.strptime(x,'%Y-%m-%d'))
    zenodo['since'] = 12 * (
        zenodo['starts_at'].dt.year-
        zenodo['created_at'].dt.year
        ) + (
        zenodo['starts_at'].dt.month-
        zenodo['created_at'].dt.month
        )
    zenodo['downloads_per_month'] = zenodo['downloads']/zenodo['since']
    zenodo.sort_values('id')
    zenodo.drop(['created_at','starts_at','views'], axis=1,inplace=True)
    return zenodo


def label_specific_papers(zenodo:pd.DataFrame) -> pd.DataFrame:
    '''
    
    '''
    zenodo.loc[zenodo['id'] == 5259883,'lbl'] = "Geography and Agricultural Productivity"
    zenodo.loc[zenodo['id'] == 4619197,'lbl'] = "Quasi-Experimental Shift-Share Research Designs"
    zenodo.loc[zenodo['id'] == 4448256,'lbl'] = "Identifying Shocks via Time-Varying Volatility"
    zenodo.loc[zenodo['id'] == 4773516,'lbl'] = "Skill-Biased Structural Change"
    zenodo.loc[zenodo['id'] == 3997900,'lbl'] = "Trade and Domestic Production Networks"
    zenodo.loc[zenodo['id'] == 5104830,'lbl'] = "Measuring the Incentive to Collude"

    return zenodo



def create_zenodo_data(path_2022:str, path_2021:str) -> pd.DataFrame:
    '''
    
    '''
    zenodo22 = pd.read_csv(path_2022)
    zenodo22 = manipulate_zenodo22(zenodo22)
    creation_time = zenodo22[['id', 'created_at']]
    zenodo21 = pd.read_csv(path_2021)
    zenodo21 = manipulate_zenodo21(zenodo21)
    zenodo21 = zenodo21.merge(creation_time,how='left', on='id')

    zenodo = pd.concat((zenodo21,zenodo22))
    zenodo = manipulate_merged_zenodo(zenodo)
    
    zenodo21 = zenodo[zenodo.year=="2021"]
    zenodo21.drop('year',axis=1,inplace=True)
    zenodo21.columns = [col+'2021' if col != 'id' else col for col in zenodo21.columns]
    zenodo22 = zenodo[zenodo.year=="2022"]
    zenodo22.drop('year',axis=1,inplace=True)
    zenodo22.columns = [col+'2022' if col != 'id' else col for col in zenodo22.columns]

    zenodo_wide = zenodo22.merge(zenodo21, how='left', on='id')
    zenodo_wide = label_specific_papers(zenodo_wide)

    return zenodo_wide

def time_at_editor_chart(data:pd.DataFrame) -> go.Figure:
    '''

    '''
    time_at_editor_chart = go.Figure()
    time_at_editor_chart.add_trace(go.Histogram(
            x=data[data['revision']==0]['time_at_editor'],
            hovertemplate="Bin:%{x} - %{y}",
            name='First submission',
            )
        )
    time_at_editor_chart.add_trace(go.Histogram(
            x=data[data['revision']>0]['time_at_editor'],
            hovertemplate="Bin:%{x} - %{y}",
            name='Revision',
        )
    )
    time_at_editor_chart.update_layout(
        title={
                "text": f"Time at editor",
                },
        font = dict(
                size = 14
                ),
        showlegend = True,
        hoverlabel = dict(
                font_size = 14,
                font_family = "Rockwell"
            ),
        barmode='overlay',
        xaxis_title_text='Days at editor',
        yaxis_title_text='Frequency',
    )
    time_at_editor_chart.update_traces(opacity=0.5)
    return time_at_editor_chart

def revisions_chart(data:pd.DataFrame) -> go.Figure:
    '''
    
    '''
    revisions_chart = go.Figure(data = go.Histogram(
                x=data[data['revision']==0]['max_revision'],
                hovertemplate="%{y}<extra></extra>"
            )
        )
    revisions_chart.update_layout(
        title={
                "text": f"Number of revision round for accepted packages",
                },
        font = dict(
                size = 14
                ),
        showlegend = False,
        hoverlabel = dict(
                font_size = 14,
                font_family = "Rockwell"
            ),
        barmode='overlay',
        xaxis_title_text='Accepted revison',
        yaxis_title_text='Frequency',
    )
    revisions_chart.update_traces(opacity=0.5)
    return revisions_chart

def revisions_year_chart(data:pd.DataFrame) -> go.Figure:
    '''
    
    '''
    revision_years_chart = go.Figure()
    revision_years_chart.add_trace(go.Bar(
            x=data.loc[data['year']==2021,'max_revision'],
            y=data.loc[data['year']==2021,'percent'],
            hovertemplate="%{y:.1%}",
            name='2021',
            )
        )
    revision_years_chart.add_trace(go.Bar(
            x=data.loc[data['year']==2022,'max_revision'],
            y=data.loc[data['year']==2022,'percent'],
            hovertemplate="%{y:.1%}",
            name=2022,
        )
    )
    revision_years_chart.add_trace(go.Bar(
            x=data.loc[data['year']==2023,'max_revision'],
            y=data.loc[data['year']==2023,'percent'],
            hovertemplate="%{y:.1%}",
            name=2023,
        )
    )
    revision_years_chart.add_trace(go.Bar(
            x=data.loc[data['year']==2024,'max_revision'],
            y=data.loc[data['year']==2024,'percent'],
            hovertemplate="%{y:.1%}",
            name=2024,
        )
    )
    revision_years_chart.update_layout(
        title={
                "text": f"Number of revisions needed in 2021-23",
                },
        font = dict(
                size = 14
                ),
        showlegend = True,
        hoverlabel = dict(
                font_size = 14,
                font_family = "Rockwell"
            ),
        barmode='group',
        xaxis_title_text='Revisions needed',
        yaxis_title_text='Percentage',
    )
    revision_years_chart.update_traces(opacity=0.5)
    return revision_years_chart

def main_issues_chart(data:pd.DataFrame) ->go.Figure:
    '''
    
    '''
    main_issues_chart = go.Figure(data=go.Scatter(
        x=data['value'],
        y=data['issue'],
        hovertemplate="%{x}<extra></extra>",
        orientation='h',
        mode='markers'
        )
    )
    for i in range(data.shape[0]):
        main_issues_chart.add_shape(
            type='line',
            x0=0, y0=data.loc[i,'issue'], 
            x1=data.loc[i,'value'], y1=data.loc[i,'issue'], 
            line_color="#cccccc"
        )

    main_issues_chart.update_layout(
        title={
                "text": f"Main issues during revision of packages",
                },
        font = dict(
                size = 14
                ),
        showlegend = False,
        hoverlabel = dict(
                font_size = 14,
                font_family = "Rockwell"
            ),
        xaxis_title_text='Percent',
    )
    main_issues_chart.update_traces(marker_size=10)
    return main_issues_chart

def downloads_chart(data:pd.DataFrame) -> go.Figure:
    '''
    
    '''
    downloads_chart = go.Figure(data=go.Scatter(
        x=data['downloads_per_month2022'],
        y=data['downloads_per_month2021'],
        hovertemplate="2021-2022<extra></extra>",
        mode='markers',
        name='2021-2022'
        )
    )

    downloads_chart.add_trace(go.Scatter(
        x=data['downloads_per_month2023'],
        y=data['downloads_per_month2021'],
        hovertemplate="2021-2023<extra></extra>",
        mode='markers',
        name='2021-2023'
        )
    )

    downloads_chart.add_trace(go.Scatter(
        x=data['downloads_per_month2024'],
        y=data['downloads_per_month2021'],
        hovertemplate="2021-2024<extra></extra>",
        mode='markers',
        name='2021-2024'
        )
    )

    downloads_chart.add_trace(go.Scatter(
        x=data['downloads_per_month2023'],
        y=data['downloads_per_month2022'],
        hovertemplate="2022-2023<extra></extra>",
        mode='markers',
        name='2022-2023'
        )
    )

    downloads_chart.add_trace(go.Scatter(
        x=data['downloads_per_month2024'],
        y=data['downloads_per_month2022'],
        hovertemplate="2022-2024<extra></extra>",
        mode='markers',
        name='2022-2024'
        )
    )

    downloads_chart.add_trace(go.Scatter(
        x=data['downloads_per_month2024'],
        y=data['downloads_per_month2023'],
        hovertemplate="2022-2023<extra></extra>",
        mode='markers',
        name='2023-2024'
        )
    )

    downloads_chart.update_layout(
        title={
                "text": f"Package Downloads by years",
                },
        font = dict(
                size = 14
                ),
        showlegend = True,
        hoverlabel = dict(
                font_size = 14,
                font_family = "Rockwell"
            ),
        xaxis_title_text='Downloads per month',
        yaxis_title_text='Downloads per month',
    )
    downloads_chart.update_traces(marker_size=10,opacity=0.5)
    return downloads_chart

def downloads_per_month_chart(data:pd.DataFrame) -> go.Figure:
    '''
    
    '''
    downloads_per_month_chart = go.Figure(data = go.Histogram(
                x=data['downloads_per_month2022'],
                hovertemplate="%{x} : %{y}<extra></extra>",
                xbins=dict(
                    start=0,
                    end=9,
                    size=1
                ),
                name='2022'
            )
        )
    
    downloads_per_month_chart.add_trace(
            go.Histogram(
                x=data['downloads_per_month2023'],
                hovertemplate="%{x} : %{y}<extra></extra>",
                xbins=dict(
                    start=0,
                    end=9,
                    size=1
                ),
                name='2023'
            )
        )
    
    downloads_per_month_chart.add_trace(
            go.Histogram(
                x=data['downloads_per_month2024'],
                hovertemplate="%{x} : %{y}<extra></extra>",
                xbins=dict(
                    start=0,
                    end=9,
                    size=1
                ),
                name='2024'
            )
        )

    downloads_per_month_chart.update_layout(
        title={
                "text": f"Downloads per months in each year from 2022",
                },
        font = dict(
                size = 14
                ),
        showlegend = True,
        hoverlabel = dict(
                font_size = 14,
                font_family = "Rockwell"
            ),
        xaxis_title_text='Downloads per month',
        barmode='overlay'
    )
    downloads_per_month_chart.update_traces(opacity=0.3)
    return downloads_per_month_chart

def top_table(data:pd.DataFrame, filter:str) -> go.Figure:
    '''
    
    '''
    table = data.sort_values(
                    filter, ascending=False
                ).drop(
                    'year',axis=1
                ).reset_index(
                    drop=True
                ).head()

    odd_row='white'
    even_row='lightgrey'
    table_chart = go.Figure()
    table_chart.add_trace(
        go.Table(
            header = dict(
                        values=list(table.columns),
                        line_color='darkslategray',
                        fill_color='royalblue',
                        align=['left','center'],
                        font=dict(color='white', size=12),
                        height=40
                    ),
            cells = dict(
                        values = [table.loc[:,col] for col in table.columns],
                        line_color='darkslategray',
                        fill_color = [[odd_row,even_row]*40],
                        align=['left', 'center'],
                        font_size=12,
                        height=30
                    )
        )
    )
    table_chart.update_layout(
        title={
                "text": f"Top 5 time spent in queue by {filter}",
                },
        )

    return table_chart