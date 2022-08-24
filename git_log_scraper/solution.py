import os
import csv

#Dummy Blank CSV for adding newline in csv module
dummy = "dummy.csv"

#Loop through your set of repos 
list = ["Code repo 1", "Code repo 2"]
for repo in list:
    os.chdir(repo)
    # git pull all the remote origin updates from all branches
    cmd1 = "git pull --all".format(repo)
    os.system(cmd1)
    #git log all (for initial log) & then update it with --after=<date> (from a specified date - you can automate/schedule it)
    cmd2 = "git log --all --after=2021-06-10 --pretty=format:'{},%h,%an,%ad,%s' > {}.csv".format(repo,repo)
    os.system(cmd2)
    src = "{}.csv".format(repo)
    #To append here as CSV I have used csv module
    tf = open('<Path:>/Gitlog-output.csv', 'a+', newline="")
    if os.path.getsize('<Path:>/{}.csv'.format(repo)) != 0:
        #Writing each git log data to the above output file and conditional newline if there isn't a commit in any branch.
        tf.write(open(src).read())
        tf.write(open(dummy).read())
    tf.close()

    print("Finished logging {}".format(repo))
    # To track the list of remaining repos from your list
    print("Remaining Repos: {}".format(len(list) - list.index(repo) -1 ))
    print("#####################################")