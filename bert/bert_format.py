"""
Takes a json files of games and returns a json ready for BERT
"""
import os 
import json 
import datetime

current_folder=os.getcwd()

open_path = current_folder + '/json_in/'

save_path= current_folder + '/json_out/'

json_files = os.listdir(open_path)

output_list = []

with_relations = 0
split = 'dev'
annotation_level = 'BRONZE'

for f in json_files:
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            game_dict = {}
            #get id
            game_dict['id'] = game['game_id']
            
            edus = []
            for elem in game['edus']:
                edict = {k: v for k, v in elem.items() if k in ['text', 'Speaker']}
                print(game['game_id'])
                edict['speaker'] = edict.pop('Speaker')
                print(edict)
                edus.append(edict)
            
            game_dict['edus'] = edus
            
            if with_relations:
                relations = []
                ##make id index dict -- WIP: need to make sure flattening takes this into account
                # id_to_index = {elem['unit_id']: elem['global_index'] for elem in game['edus']}
                ##WIP -- make sure relations are spelled the same
                for rel in game['relations']:
                    rdict = {k: v for k, v in rel.items() if k in ['x', 'y', 'type']}
                    relations.append(rdict)
            else:
                relations = []

            game_dict['relations'] = relations

            output_list.append(game_dict)

    print('{} {} games formatted.'.format(len(output_list), split))    

    now = datetime.datetime.now().strftime("%Y-%m-%d")

    ##save bert json
    with open(save_path + now + annotation_level + '_' + split + '_bert.json', 'w') as outfile:
        json.dump(output_list, outfile)

    print('json saved')

            
            