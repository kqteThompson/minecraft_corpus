"""
Takes a json file of ANNOTATED games that have been flattened 
and squished.
Returns json ready for BERT
"""
import os 
import json 
import datetime

current_folder=os.getcwd()

# open_path = current_folder + '/json_in/'
open_path = '/home/kate/minecraft_corpus/flatten/json_squishflat/'

save_path= current_folder + '/json_out/'

json_files = os.listdir(open_path)

output_list = []

with_relations = 1
builder_names_replace = 0
split = 'dev'
annotation_level = 'BRONZE'

for f in json_files:
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile: #only use 10 games for testing purposes
            game_dict = {}
            #get id
            game_dict['id'] = game['game_id']
            print(game['game_id'])
            edus = []
            sorted_edus = sorted(game['edus'], key=lambda d: d['start_pos']) 
            #sort the edus so that they are sure to be in the correct order
            for elem in sorted_edus:
                edict = {k: v for k, v in elem.items() if k in ['text', 'Speaker']}
                edict['speaker'] = edict.pop('Speaker')
                #change builder and speaker 
                edict['speaker'] = edict['speaker'].split('_')[0]
                edus.append(edict)
            
            game_dict['edus'] = edus
            
            if with_relations:
                index_dict = {}
                counter = 0
                for elem in sorted_edus:
                    # index_dict[elem['unit_id']] = elem['global_index'] ##but these might be out of order!!
                    index_dict[elem['unit_id']] = counter
                    counter += 1
                relations = []
                ##make id index dict -- WIP: need to make sure flattening takes this into account
                # id_to_index = {elem['unit_id']: elem['global_index'] for elem in game['edus']}
                ##WIP -- make sure relations are spelled the same
                for rel in game['relations']:
                    rdict = {}
                    rdict['x'] = index_dict[rel['x_id']]
                    rdict['y'] = index_dict[rel['y_id']]
                    rdict['type'] = rel['type']
                    relations.append(rdict)
            else:
                relations = []

            game_dict['relations'] = relations

            if builder_names_replace == 1:
                #go through all edus and replace 'System' speaker with 'Builder'
                for edu in game_dict['edus']:
                    if edu['speaker'] == 'System':
                        edu['speaker'] = 'Builder'

            output_list.append(game_dict)

    print('{} {} games formatted.'.format(len(output_list), split))    

    now = datetime.datetime.now().strftime("%Y-%m-%d")

    ##save bert json
    save_file_name = save_path + now + annotation_level + '_' + split +'_bert.json'
    
    with open(save_file_name, 'w') as outfile:
        json.dump(output_list, outfile)

    print('json saved')

            
            