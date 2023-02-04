"""
this will take ac and aa glozz files for each game and output a json 
file with the edu, cdu, and relation information for each game.
"""

import os
import xml.etree.ElementTree as ET
import json
import datetime

annotation_level = 'BRONZE' #whichever level
current_folder=os.getcwd()

#if these folders don't exist in directory change paths accordingly
aa_path = current_folder + '/aa_files/'
ac_path = current_folder + '/ac_files/'

save_path= current_folder + '/json_output/'
if not os.path.isdir(save_path):
    os.makedirs(save_path)

aa_list = os.listdir(aa_path)

all_games = []

for aa in aa_list:

    game = {}
    game_id = aa.split('.')[0]
    game['game_id'] = game_id
    print("working on game ", game_id)
    edus = []
    relations = []
    cdus = []
    
    aa_file_path = aa_path + aa
    tree = ET.parse(aa_file_path)
    root = tree.getroot()

    count = 0
    #get all units
    for elem in root.iter('unit'):
        for type in elem.iter('type'):
            if type.text == 'Segment':
                edu = {}
                edu['unit_id'] = elem.attrib['id']
                for feature in elem.iter('feature'):
                    edu[feature.attrib['name']] = feature.text
                positions = [pos.attrib['index'] for pos in elem.iter('singlePosition')]
                edu['start_pos'] = int(positions[0])
                edu['end_pos'] = int(positions[1])
                edu['global_index'] = count
                count +=1 
                edus.append(edu)

    #get all relations
    for elem in root.iter('relation'):
        relation = {}
        relation['relation_id'] = elem.attrib['id']
        for type in elem.iter('type'):
            relation['type'] = type.text
        segs = [unit.attrib['id'] for unit in elem.iter('term')]
        relation['x_id'] = segs[0]
        relation['y_id'] = segs[1]
        relations.append(relation)
    
    #get all cdus
    for elem in root.iter('schema'):
        schema = {}
        schema['schema_id'] = elem.attrib['id']
        unit_list = []
        for edu in elem.iter('embedded-unit'):
            unit_list.append(edu.attrib['id'])
        schema['embedded_units'] = unit_list
        cdus.append(schema)

    #add edu (and cdu!) indicies to relations
    edu_index_dict = {}
    for edu in edus:
        edu_index_dict[edu['unit_id']] = edu['global_index']

    cdu_indicies = [cdu['schema_id'] for cdu in cdus]
    for cdu in cdus:
        edu_index_dict[cdu['schema_id']] = 'cdu_' + str(count)
        count += 1

    for relation in relations:
        relation['x'] = edu_index_dict[relation['x_id']]
        relation['y'] = edu_index_dict[relation['y_id']]
    

    #add text from ac file
    with open(ac_path + game_id + '.ac', 'r') as txt:
        text = txt.read().replace('\n', '')
        for unit in edus:
            unit_text = text[unit['start_pos']:unit['end_pos']]
            unit['text'] = unit_text

    game['edus'] = edus
    game['relations'] = relations
    game['cdus'] = cdus
    all_games.append(game)
    print("finished game ", game_id)

##save json
now = datetime.datetime.now().strftime("%Y-%m-%d")

with open(save_path + annotation_level + '_' + now + '.json', 'w') as outfile:
    json.dump(all_games, outfile)

print('json saved')




    


