"""
Takes a json file of ANNOTATED games that have been flattened 
and squished.
splits into multiple json files according to split
"""
import os 
import json 
import datetime

current_folder=os.getcwd()

# open_path = current_folder + '/json_in/'
open_path = '/home/kate/minecraft_corpus/flatten/json_squishflat/'

save_path= current_folder + '/json_in/'

json_files = os.listdir(open_path)

test_games = ['C1', 'C14', 'C36']

test_list = []
train_list = []

split = 'dev'
annotation_level = 'SILVER'

for f in json_files:
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            if game['game_id'].split('-')[0] in test_games:
                test_list.append(game)
            else:
                train_list.append(game)

for l in [test_list, train_list]:

    num_games = str(len(l))

    print('{} games formatted.'.format(num_games))    

    now = datetime.datetime.now().strftime("%Y-%m-%d")

    ##save bert json
    save_file_name = save_path + now + '_' + annotation_level + '_' + split + '_' + num_games + '_bert.json'

    with open(save_file_name, 'w') as outfile:
        json.dump(l, outfile)

    print('json saved')




       