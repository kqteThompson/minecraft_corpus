"""
this will take ac and aa glozz files for each game and output a json 
file with the edu, cdu, and relation information for each game.
"""

import os
import xml.etree.ElementTree as ET
import json
import datetime

annotation_level = 'SILVER' #whichever level
current_folder=os.getcwd()

#if these folders don't exist in directory change paths accordingly

# ac_path = current_folder + '/ac_files/'
ac_path = current_folder + '/ac_files/'
# ac_path = '/home/kate/glozz_platform/glozz-platform-dist-2.1/minecraft_data/corpus/'

# aa_path = current_folder + '/aa_files/'
# aa_path = current_folder + '/test_aa_files/'
# aa_path = current_folder + '/all_aa/'
aa_path = '/home/kate/glozz_platform/glozz-platform-dist-2.1/minecraft_data/dev_set/'

save_path= current_folder + '/json_output/'

if not os.path.isdir(save_path):
    os.makedirs(save_path)

aa_list = os.listdir(aa_path)

all_games = []

for aa in aa_list:

    pass_flag = False
    error_msg = None

    game = {}
    game_id = ''
    #fix this
    game_id = aa.split('.')[0]
    game['game_id'] = game_id
    print("working on game ", game_id)
    paragraphs = []
    edus = []
    relations = []
    cdus = []# print(e)
    embedded_cdus = []
    speaker_dict = {} #create in case need to add speaker info
    
    aa_file_path = aa_path + aa
    tree = ET.parse(aa_file_path)
    root = tree.getroot()

    count = 0
    # #get all paragraph units
    # for elem in root.iter('unit'):
    #     for type in elem.iter('type'):
    #         if type.text == 'paragraph':
    #             para = {}
    #             para['unit_id'] = elem.attrib['id']
    #             positions = [pos.attrib['index'] for pos in elem.iter('singlePosition')]
    #             para['start_pos'] = int(positions[0])
    #             para['end_pos'] = int(positions[1])
    #             paragraphs.append(para)

    # #get all edu units
    # for elem in root.iter('unit'):
    #     for type in elem.iter('type'):
    #         if type.text == 'Segment':
    #             edu = {}
    #             edu['unit_id'] = elem.attrib['id']
    #             for feature in elem.iter('feature'):
    #                 edu[feature.attrib['name']] = feature.text
    #             positions = [pos.attrib['index'] for pos in elem.iter('singlePosition')]
    #             edu['start_pos'] = int(positions[0])
    #             edu['end_pos'] = int(positions[1])
    #             if edu['start_pos'] != edu['end_pos']: #skip empty edus
    #                 edu['global_index'] = count
    #                 count +=1 
    #                 edus.append(edu)
    
    last_para_id = None
    for elem in root.iter('unit'):
        for type in elem.iter('type'):
            if type.text == 'paragraph':
                last_para_id = elem.attrib['id']
                para = {}
                para['unit_id'] = last_para_id
                positions = [pos.attrib['index'] for pos in elem.iter('singlePosition')]
                para['start_pos'] = int(positions[0])
                para['end_pos'] = int(positions[1])
                paragraphs.append(para)
            if type.text == 'Segment':
                edu = {}
                edu['unit_id'] = elem.attrib['id']
                edu['para_id'] = last_para_id
                for feature in elem.iter('feature'):
                    edu[feature.attrib['name']] = feature.text
                    if feature.attrib['name'] == 'Speaker':
                        speaker_dict[last_para_id] = feature.text ##add to speaker dict
                positions = [pos.attrib['index'] for pos in elem.iter('singlePosition')]
                edu['start_pos'] = int(positions[0])
                edu['end_pos'] = int(positions[1])
                if edu['start_pos'] != edu['end_pos']: #skip empty edus
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
        #take account of embedded-schema -- need try catch?
        for cdu in elem.iter('embedded-schema'):
            unit_list.append(cdu.attrib['id'])
            embedded_cdus.append((elem.attrib['id'], cdu.attrib['id']))

        schema['embedded_units'] = unit_list
        cdus.append(schema)

    #check for edus without Speakers (this happens when they are split manually)
    #add speaker information
    for edu in edus:
        if 'Speaker' not in edu.keys():
            #find speaker based on para id
            edu['Speaker'] = speaker_dict[edu['para_id']]
            edu['minecraftSegID'] = edu['unit_id'] + '_' + speaker_dict[edu['para_id']]
            ##NB we don't add turn ids
            print('added speaker infor to edu {} in {}'.format(edu['unit_id'], game_id))

    #add edu (and cdu!) indicies to relations
    edu_index_dict = {}
    for edu in edus:
        edu_index_dict[edu['unit_id']] = edu['global_index']

    cdu_indicies = [cdu['schema_id'] for cdu in cdus]
    for cdu in cdus:
        edu_index_dict[cdu['schema_id']] = 'cdu_' + str(count)
        count += 1

    for relation in relations:
        try:
            relation['x'] = edu_index_dict[relation['x_id']]
            relation['y'] = edu_index_dict[relation['y_id']]
        except KeyError as e:
            error_msg = e
            pass_flag = True
            print("pass flag on", relation['x_id'])
    
    if pass_flag:
        print("relation issue in {}".format(error_msg))
        print("skipping file.")
        pass_flag = False
        pass
    
    #add text from ac file
    with open(ac_path + game_id + '.ac', 'r') as txt:
        text = txt.read().replace('\n', '')
        for unit in edus:
            unit_text = text[unit['start_pos']:unit['end_pos']]
            unit['text'] = unit_text

    #add embedded CDUs if there are any
    final_embed = []
    if len(embedded_cdus) > 0:
        for cdu in embedded_cdus:
            embed_dict = {}
            embed_dict['parent_id'] = cdu[0]
            embed_dict['child_id'] = cdu[1]
            final_embed.append(embed_dict)
    
    game['paras'] = paragraphs
    game['edus'] = edus
    game['relations'] = relations
    game['cdus'] = cdus
    game['embedded_cdus'] = final_embed
    all_games.append(game)
    print("finished game ", game_id)

##save json
now = datetime.datetime.now().strftime("%Y-%m-%d")

with open(save_path + annotation_level + '_' + now + '.json', 'w') as outfile:
    json.dump(all_games, outfile)

print('json saved')
