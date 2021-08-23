# Trello to JSON code

Base of the code is at https://github.com/deal2k/trello_json_to_csv

## How to use?

1. The .json file is not included in the git repo. However, to run the scripts export a trello board as json and save it in the folder of the code.
2. The `trello_json_to_csv.py` is a class, but in default running the script creates a .csv from an exported .json trello board. 
3. If you want to use a differnet trello board then *REStud replications* tweak the appropriate parts of the code.

## Output

The output is in longformat, meaning that the cards are the columns and the rows are some attributes and the histories of the cards. Currently the script only keeps the __createCard__ and __updateCard__ actions, because under these actions happened the list changes that are the most important for now.