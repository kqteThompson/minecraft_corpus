'''
input: a json with edus and bert relation predictions
NB: this file just feeds one game dict at a time to the get_format function
output: folder with .aa and .ac files for each game in json
'''
import os
from genglozzsegments import get_format
import json

predicted_relations = 'bert_pred.json'

current_folder=os.getcwd()

json_path = current_folder + '/' + predicted_relations

save_path= current_folder + '/glozz/'
if not os.path.isdir(save_path):
    os.makedirs(save_path)

with open(json_path, 'r') as jf:
    preds = json.load(jf)

for game in preds:
    ac_file, aa_file, dialogue_id = get_format(game)
    with open (save_path + '/' + dialogue_id + '_bert.aa', 'w') as xml_file:
        xml_file.write(aa_file)
    with open (save_path + '/' + dialogue_id + '_bert.ac', 'w') as text_file:
        text_file.write(ac_file)
    print('dialogue done', dialogue_id)

                    
            
               