import time
import pandas as pd

START_DATE = '2019-01-01'
END_DATE = '2022-09-05'

def unix_time(datetime:str) -> int:
    ''' '''
    date = time.strptime(datetime, '%Y-%m-%d')
    return int(time.mktime(date))

def create_marks(start:str=START_DATE, end:str=END_DATE, n:int=4) -> dict:
    '''
    
    '''
    results = {}
    daterange = pd.date_range(start, end, freq='W')
    for i, date in enumerate(daterange):
        if (i%n==0):
            results[unix_time(str(date).split(' ')[0])] = str(date.strftime('%Y-%m-%d'))

    return results
