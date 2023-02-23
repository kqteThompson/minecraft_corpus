"""
Takes a json files of games and returns a json with flattened games
"""
import os 
import json 

current_folder=os.getcwd()

open_path = current_folder + '/json/'

save_path= current_folder + '/json_flat/'

json_files = os.listdir(open_path)

for f in json_files:
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            replacements = {}
            print(game['game_id'])
            edus = [(e['unit_id'], e['start_pos']) for e in game['edus']]
            cdus = game['cdus']
            #for each cdu 
            for cdu in cdus:
                cid = cdu['schema_id']
                elements = [elem for elem in edus if elem[0] in cdu['embedded_units']]
                first = min(elements, key=lambda tup: tup[1])
                head = first[0]
                replacements[cid] = head
            #once you have your replacements, replace relation nodes
            for rel in game['relations']:
                if rel['x_id'] in replacements:
                    rel['x_id'] = replacements[rel['x_id']]
                if rel['y_id'] in replacements:
                    rel['y_id'] = replacements[rel['y_id']]

            #remove cdu field

            game['cdus'] = []
    ##re-save a new json

    with open(save_path + f + '_flattened.json', 'w') as outfile:
        json.dump(jfile, outfile)

    print('json saved')

            
            