import os
import csv
import re

def parse_report(repo:str, path:str):
  '''
  Parse report of version1 branch and export it to csv.
  -------------------------------------------------
  Input: Manuscript ID as string
  Output: A row in the csv file
  '''
  temp_ans=[]
  temp_ans.append(repo)
  os.system("git switch version1")

  try:
    with open('report.yaml','r') as rf:
      report = rf.read()

    req_rec = re.findall(r"-\s(.*)", report)
    for resp in req_rec:
      match = re.match(r"\*(.*)", resp)
      if match is not None:
        if match.group() not in ['*relative_path', '*forward_slash', '*macosx']:
            temp_ans.append(match.group().split("*")[1].split(" ")[0])

    with open(path, 'a+') as f:
      writer = csv.writer(f)
      writer.writerow(temp_ans)
  
  except FileNotFoundError:
    pass

def clone(repo_url:str):
  '''
  Clones given repo from url.
  '''
  os.system("git clone {}".format(repo_url))

def logger(repo:str):
  '''
  Create csv from git log output, and parse report.
  -------------------------------------------------------
  Input: repo MS id number as string
  Output: csv format of git commits, csv fromat of report template answer labels
  '''
  os.chdir(repo)
  cmd = "git log --all --pretty=format:'{},%h,%an,\"%ad\",\"%s\",\"%d\"' > {}.csv".format(repo,repo)
  os.system(cmd)
  parse_report(repo,"../../output/report_labs.csv")
  os.chdir("..")

def countrow(path:str) -> int:
  '''
  Count rows in a file.
  ------------------------------
  Input: path as a string
  Output: number of rows 
  '''
  rowcount=0
  for row in open(path,'r'):
    rowcount+=1
  return rowcount

def main():
  #find a file that is the list of repos.
  gh_list = "temp/gh_list.csv"
  rowcount=countrow(gh_list)
  #iterating through the whole file
  tf = open('output/Gitlog-output.csv', 'a+', newline="\n")
  tf.write('MS,commit,author,date,message,branch')

  with open(gh_list, 'r') as csvfile:
    reader = csv.reader(csvfile)
    os.chdir("temp")
    for repo in reader:
        # # git pull all the remote origin updates from all branches
        clone(repo[1])
        # #git log all (for initial log) & then update it with --after=<date> (from a specified date - you can automate/schedule it) + log report temp answers
        logger(repo[0])
        # #To append here as CSV I have used csv module
        tf = open('../output/Gitlog-output.csv', 'a+', newline="\n")
        src = '{}/{}.csv'.format(repo[0],repo[0])
        if os.path.getsize(src) != 0:
        # #Writing each git log data to the above output file and conditional newline if there isn't a commit in any branch.
            tf.write('\n')
            tf.write(open(src).read())
        tf.close()

        cmd_clr = "rm -rf {}".format(repo[0])
        os.system(cmd_clr)

        print("Finished logging {}".format(repo[0]))
        # To track the list of remaining repos from your list
        rowcount = rowcount -1
        print("Remaining Repos: {}".format(rowcount))
        print("#####################################")

if __name__ == '__main__':
  main()