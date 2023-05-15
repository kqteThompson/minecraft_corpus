'''
input: a json with edus and bert relation predictions from linear model
NB: this file just feeds one game dict at a time to the get_format function
output: folder with .aa and .ac files for each game in json
'''
import os
from genglozzsegments import get_format, builder_to_system
import json

predicted_relations = 'bert_multi_coord_preds_rels.json'

current_folder=os.getcwd()

json_path = current_folder + '/' + predicted_relations


save_path= current_folder + '/glozz_multi_pred_coords/'
if not os.path.isdir(save_path):
    os.makedirs(save_path)

with open(json_path, 'r') as jf:
    preds = json.load(jf)

for game in preds:
    #change builder to system
    game_new = builder_to_system(game)
    ac_file, aa_file, dialogue_id = get_format(game_new)
    with open (save_path + '/' + dialogue_id + '_multicoord.aa', 'w') as xml_file:
        xml_file.write(aa_file)
    with open (save_path + '/' + dialogue_id + '_multicoord.ac', 'w') as text_file:
        text_file.write(ac_file)
    print('dialogue done', dialogue_id)

                    
            
               