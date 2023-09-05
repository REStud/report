import pandas as pd
import numpy as np
SEED = 2023071

def take_random_sample(size:int)-> pd.DataFrame:
    '''
    Takes a random smaple from the version1 report labels
    '''
    data = pd.read_stata('output/report_labs.dta')
    generator = np.random.default_rng(seed=SEED)
    random_array = generator.integers(low=0,high=data.shape[0]-1,size=size)
    data = data.loc[random_array,:]
    return data

def create_analysis_sample(data:pd.DataFrame) -> pd.DataFrame:
    lab_cols = data.columns[1:]
    labels = set()

    for col in data:
        if col.startswith('lab'):
            labels = labels.union(set(data[col].dropna().unique()))

        
    for label in labels:
        data[label] = 0
        for col in data:
            data[label] = data[label] + data[col].apply(lambda x: x == label)
            
    data.drop(lab_cols,axis=1, inplace=True)
    data.to_csv("temp/analysis_sample.csv")
    return data

def plot_issues(data:pd.DataFrame):
    for col in data:
        data['col'].sum().plot()

def main():
    df = take_random_sample(size=50)
    analysis_df = create_analysis_sample(data=df)
    print(analysis_df)

if __name__=='__main__':
    main()

