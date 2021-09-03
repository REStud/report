# script to export Trello JSON to CSV format
# data to capture: name (card), status, label, activity (data, user, info)
import pandas as pd
import json

class Exporter(object):
    def __init__(self, board, actions):
        self.file = board
        self.actions = actions
        with open(self.file+'.json', 'r') as json_file:
            self.json_data = json.load(json_file)

        with open(self.actions+'.json', 'r') as actions_file:
            self.actions = json.load(actions_file)

    def lists_to_df(self):
        self.lists_df = pd.DataFrame(self.json_data['lists']).loc[:, ['id', 'name']].set_index('id')
        

    def cards_to_df(self):
        columns = ['id', 'idList', 'closed', 'name', 'labels']
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
        self.cards = pd.merge(self.cards, self.lists_df, how='left', left_on='idList', right_on='id', 
                     suffixes=('_card', '_list'), right_index=True).drop(['idList'], axis=1)

    def actions_to_df(self):
        columns = ['idMemberCreator','data','type','date']
        self.actions = pd.DataFrame(self.actions)
        self.actions = self.actions.sort_values(by='date').reset_index(drop=True)
        self.actions = self.actions.sort_values(by='date').reset_index(drop=True)
    
    def remove_action_duplicates(self):
        self.actions = self.actions.drop_duplicates(subset=['id','date','type','list_after','list_before']).reset_index()

    def fill_up_actions(self):
        # prepare new columns
        self.actions['card_id'] = ''
        self.actions['list_before'] = ''
        self.actions['list_after'] = ''

        # add info to DataFrame
        for row in range(len(self.actions)):
            self.actions.loc[row, 'card_id'] = self.actions.loc[row, 'data']['card']['id']
            try:
                self.actions.loc[row, 'list_before'] = self.actions.loc[row, 'data']['listBefore']['name']
                self.actions.loc[row, 'list_after'] = self.actions.loc[row, 'data']['listAfter']['name']
            except KeyError:
                self.actions.loc[row, 'list_before'] = ''
                self.actions.loc[row, 'list_after'] = ''

    def export_to_csv(self):
        # create table for export
        self.cards_list = []
        for row in range(len(self.cards)):
            # prepare empty dictionary
            card = {}
            
            # add name of card (task)
            card['name'] = self.cards.iloc[row,1]
            
            # add status
            card['status'] = 'Open'
            if self.cards.iloc[row, 0] == True:
                card['status'] = 'Closed'
            
            # add name of list (bucket)
            card['list'] = self.cards.iloc[row, 3]
            
            # add label
            card['label'] = self.cards.iloc[row, 2]
            
            
            # add actions to card
            # get card id
            card_id = self.cards.index[row]
            
            # iterate over list of action to find action for this card
            counter = 0
            for action_id in range(len(self.actions)):
                if self.actions['card_id'][action_id] == card_id:
                    card['activity' + str(counter)] = self.actions['type'][action_id]
                    card['date' + str(counter)] = self.actions['date'][action_id][:16]
                    card['list_before' + str(counter)] = self.actions['list_before'][action_id]
                    card['list_after' + str(counter)] = self.actions['list_after'][action_id]
                    counter += 1
            
            # add card dict to list of cards
            self.cards_list.append(card)
            
        # prepare new DataFrame from list of dicts
        df = pd.DataFrame(self.cards_list)
        df['id'] = range(1,len(df)+1)
        df = pd.wide_to_long(df, ['activity','date','list_before','list_after'],i="id", j="action_id")
        # export to CSV
        df.to_csv(self.file+'.csv')

if __name__ == '__main__':

    exporter = Exporter('table31aug21', 'actions')
    exporter.lists_to_df()
    exporter.cards_to_df()
    exporter.merge_cards_to_lists()
    exporter.actions_to_df()
    exporter.fill_up_actions()
    exporter.remove_action_duplicates()
    exporter.export_to_csv()