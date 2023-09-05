# Trello to JSON code

Base of the script `trello_json_to_csv.py` at https://github.com/deal2k/trello_json_to_csv.

The other (`get_action_history.py`) script is using Trello API for scraping, for that you need an API key and API token. First can be reached [here](https://trello.com/app-key), the second [here](https://trello.com/1/token/approve). For both you have to give permission for the Atlassian API to reach your trello boards. 

For further description on the trello API click [here](https://developer.atlassian.com/cloud/trello/rest/api-group-boards/#api-boards-id-get)

## How to use `trello_json_to_csv.py`?

1. The .json file is not included in the git repo. However, to run the scripts export a trello board as json and save it in the folder of the code.
2. The `trello_json_to_csv.py` is a class, but in default running the script creates a .csv from an exported .json trello board. 
3. If you want to use a different trello board then *REStud replications* tweak the appropriate parts of the code.

## How to use `get_action_history.py`?

Save the key and token in a `secrets.json` file in the same folder as the code and give the two parameters of the scrape. The first is the most recent date you want to include, while the second is the latest date you want to include. For example:

```
python3 get_action_history.py -t 2023-09-05T08:00:00.977 -s 2020-08-01T08:00:00.977
```

The output is actions.json.
## Output

The output is in longformat, meaning that the cards are the columns and the rows are some attributes and the histories of the cards. Currently the script only keeps the __createCard__ and __updateCard__ actions, because under these actions happened the list changes that are the most important for now.