import os
import csv

#Loop through the repos
gh_list = "temp/gh_list.csv"

rowcount  = 0
#iterating through the whole file
for row in open(gh_list):
  rowcount+= 1

tf = open('output/Gitlog-output.csv', 'a+', newline="\n")
tf.write('MS,commit,author,date,message,branch')

with open(gh_list, 'r') as csvfile:
    reader = csv.reader(csvfile)
    os.chdir("temp")
    for repo in reader:
        # # git pull all the remote origin updates from all branches
        cmd1 = "git clone {}".format(repo[1])
        os.system(cmd1)
        # #git log all (for initial log) & then update it with --after=<date> (from a specified date - you can automate/schedule it)
        os.chdir(repo[0])
        cmd2 = "git log --all --pretty=format:'{},%h,%an,\"%ad\",\"%s\",\"%d\"' > {}.csv".format(repo[0],repo[0])
        os.system(cmd2)
        os.chdir("..")
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