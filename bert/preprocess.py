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
open_path = '/home/kate/minecraft_corpus/flatten/json_flat/'

save_path= current_folder + '/json_in/'

json_files = os.listdir(open_path)

test_games = ['C114-B35-A44','C61-B37-A46','C96-B16-A1','C61-B15-A38','C104-B52-A27',
'C5-B1-A3', 'C121-B44-A15','C109-B19-A36','C5-B20-A10','C96-B42-A4','C5-B12-A26','C114-B16-A1',
'C67-B31-A41','C109-B34-A31','C96-B27-A25','C104-B37-A23','C125-B27-A1','C67-B1-A44','C61-B29-A26',
'C61-B3-A16','C121-B34-A38','C121-B31-A36','C125-B35-A34','C125-B44-A15','C114-B34-A38','C121-B53-A4',
'C104-B29-A34','C67-B40-A14','C121-B16-A26','C109-B35-A44']

test_list = []
train_list = []

annotation_level = 'SILVER_FLAT'

for f in json_files:
#for f in [j for j in json_files if j == '2023-05-17_squish_flat.json']: #!!!!
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            if game['game_id'] in test_games:
                test_list.append(game)
            else:
                train_list.append(game)

for l in [test_list, train_list]:

    num_games = str(len(l))

    print('{} games formatted.'.format(num_games))    

    now = datetime.datetime.now().strftime("%Y-%m-%d")

    ##save bert json
    save_file_name = save_path + now + '_' + annotation_level + '_' + num_games + '_bert.json'

    with open(save_file_name, 'w') as outfile:
        json.dump(l, outfile)

    print('json saved')




       