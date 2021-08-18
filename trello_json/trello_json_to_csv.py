# script to export Trello JSON to CSV format
# data to capture: name (card), status, label, activity (data, user, info)
import pandas as pd
import json

def read_json(file):
    with open(jsonfile+'.json', 'r') as json_file:
        json_data=json.load(json_file)
    return json_data

class Exporter(object):
    def __init__(self, json_data):
        self.json_data = json_data


    def lists_to_df(self):
        self.lists_df = pd.DataFrame(self.json_data['lists']).loc[:, ['id', 'name']].set_index('id')
        

    def cards_to_df(self):
        columns = ['id', 'idList', 'closed', 'desc', 'name', 'labels']
        self.cards = pd.DataFrame(self.json_data['cards']).loc[:, columns].set_index('id')
        cards_num = len(self.cards['labels'].values)     # get total number of cards to iterate
        # extract labels from dictionary
        card_labels = []
        for i in range(cards_num):
            try:
                card_labels.append([self.cards['labels'].values[i][j]['name'] for j in range(len(self.cards['labels'].values[i]))])
            except IndexError:
                card_labels.append("")
        self.cards['labels'] = card_labels
        

    def merge_cards_to_lists(self):
        self.cards = pd.merge(self.cards, self.lists, how='left', left_on='idList', right_on='id', 
                     suffixes=('_card', '_list'), right_index=True).drop(['idList'], axis=1)

    def actions_to_df(self,actions_to_keep):
        columns = ['idMemberCreator','data','type','date']
        self.actions = pd.DataFrame(self.json_data['actions']).loc[:, columns]
        # filter DataFrame actions and sort in chronological order
        self.actions = self.actions[self.actions['type'].isin(actions_to_keep)].reset_index(drop=True)
        actions = actions.sort_values(by='date').reset_index(drop=True)
        return actions

    def memebers_to_df(json_data):
        members = pd.DataFrame(json_data['members']).loc[:, ['id', 'username']].set_index('id')
        return members

    def merge_actions_to_members(actions, members):
        merged = pd.merge(actions, members, how='left',
                       left_on='idMemberCreator', right_on='id',
                       suffixes=('_actions', '_members')).drop(['idMemberCreator'], axis=1)
        return merged

    def fill_up_actions(actions):
        # prepare new columns
        actions['card_id'] = ''
        actions['changed'] = ''
        actions['old'] = ''
        actions['new'] = ''

        # add info to DataFrame
        for row in range(len(actions)):
            try:
                actions.loc[row, 'card_id'] = actions.loc[row, 'data']['card']['id']
                actions.loc[row, 'changed'] = list(actions.loc[row, 'data']['old'].keys())[0]
                actions.loc[row, 'old'] = list(actions.loc[row, 'data']['old'].values())
        # get value of what was changed to use it after
                changed = list(actions.loc[row, 'data']['old'].keys())[0]
                actions.loc[row, 'new'] = actions.loc[row, 'data']['card'][changed]
            except:
                pass
        return actions

    def export_to_csv(cards, actions)
        # create table for export
        cards_list = []
        for row in range(len(cards)):
            # prepare empty dictionary
            card = {}
            
            # add name of card (task)
            card['name'] = cards.iloc[row,2]
            
            # add status
            card['status'] = 'Open'
            if cards.iloc[row, 0] == True:
                card['status'] = 'Closed'
            
            # add name of list (bucket)
            card['list'] = cards.iloc[row, 4]
            
            # add label
            card['label'] = cards.iloc[row, 3]
            
            # add description
            card['desc'] = cards.iloc[row, 1]
            
            # add actions to card
            # get card id
            card_id = cards.index[row]
            
            # iterate over list of action to find action for this card
            counter = 0
            for action_id in range(len(actions)):
                if actions['card_id'][action_id] == card_id:
                    card['activity' + str(counter)] = actions['type'][action_id]
                    card['date' + str(counter)] = actions['date'][action_id][:16]
                    card['user' + str(counter)] = actions['username'][action_id]
                    counter += 1
            
            # add card dict to list of cards
            cards_list.append(card)
            
        # prepare new DataFrame from list of dicts
        df = pd.DataFrame(cards_list).set_index('name')
        # export to CSV
        df.to_csv('table17aug21.csv')

if __name__ == '__main__':
