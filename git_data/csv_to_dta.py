import pandas as pd
import datetime as dt

def branch_extractor(branch_data:list) -> str:
    '''
    Returns git branch out of the git branch/tag list of the repo.
    ---------------------------------------------------
    Input: Branch data list
    Output: Branch name
    '''
    # 1st guard clause: extraction for '->' in branch data
    if '->' in branch_data[0]:
        branch = branch_data[0].split('-> ')[1]
        return branch
    # 2nd guard clause: extraction for '/' in branch data
    if '/' in branch_data[0]:
        branch = branch_data[0].split('/')[1]
        return branch
      
    try: 
        branch = branch_data[1].split('/')[1]
    except IndexError:
        branch = ''

    return branch

def tag_extractor(branch_data:list) -> str:
    '''
    Returns git tag out of the git branch/tag list of the repo.
    ---------------------------------------------------
    Input: Branch data list
    Output: Tag name
    '''
    # Guard clause: extraction for ':' in branch data
    if ':' in branch_data[0]:
        tag = branch_data[0].split(': ')[1]
        return tag
       
    try:
        tag = branch_data[1].split(': ')[1]
    except IndexError:
        tag = ''

    return tag

def branch_imputer(report_data:pd.DataFrame) -> pd.Series:
    '''
    Imputes branch names based on previous value of the branch name based on the previous value of branch column under the same MS id.
    --------------------------------------------------------------
    Input: Report data with already given branch names and MS ids
    Output: Imputed branch
    '''
    ms_id = report_data.MS.copy()
    branch = report_data.branch.copy()
    for i in range(len(branch)):
        try:
            if ms_id[i+1] == ms_id[i] and branch[i+1] == "":
                branch[i+1] = branch[i]
        except KeyError:
            pass
    return branch

def tag_unifier(report_data:pd.DataFrame) -> pd.Series:
    '''
    Unifies accepted tag labels.
    --------------------------------------------------------------
    Input: Report data with already given tag labels.
    Output: Unified tag labels
    '''
    tag = report_data.tag.copy()
    for i in range(len(tag)):
        tag_lab = tag[i].split('-')[0]
        if tag_lab == 'accept':
            tag[i] = 'accepted'
        else:
            tag[i] = tag_lab
    return tag

def gitlog_to_dta(in_path:str, out_path:str):
    # read in
    report_data = pd.read_csv(in_path)
    # parse date
    report_data.date = report_data.date.apply(lambda x: dt.datetime.strptime(x, "%a %b %d %H:%M:%S %Y %z"))
    # fill in na branch values
    report_data.branch = report_data.branch.fillna("")
    # Create proper branch names out of the list of branch data
    report_data.branch = report_data.branch.apply(lambda x: x.strip(" (").strip(")"))
    report_data['branch_data'] = report_data.branch.apply(lambda x: x.split(","))
    report_data["branch"] = report_data.branch_data.apply(lambda x: branch_extractor(x))
    report_data["tag"] = report_data.branch_data.apply(lambda x: tag_extractor(x))
    report_data = report_data.drop(["branch_data"], axis=1)
    # Add author branch for each initial commit
    report_data.branch[(report_data.message == 'initial commit') & (report_data.branch == "")] = 'author'
    # Impute branch names
    report_data['branch_imputed'] = branch_imputer(report_data)
    report_data.tag = tag_unifier(report_data)
    #transferm datetime object to be exportable
    report_data['numeric_date'] = report_data.date.apply(lambda x: dt.datetime.timestamp(x))
    report_data['date'] = report_data.date.apply(lambda x: str(x))
    report_data.to_stata(out_path)


def main():
    gitlog_to_dta("output/Gitlog-output.csv", "output/gitlog.dta")

if __name__ == '__main__':
    main()