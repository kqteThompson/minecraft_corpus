"""
A shorter version of format_snippets in which for each snippet, we return the 
orig and the sample_ids
so that anything NOT in these is removed from the amended BAP training data

"""
import os 
import json 
import datetime
import numpy as np
from collections import defaultdict
import torch
import nltk
# from nltk.tokenize import wordpunct_tokenize
from world_state import get_next_builder_actions, get_instruction, return_state_info, get_built_config
from prashant import get_perspective_coord_repr, tokenize, BuilderAction
from gen_splits import get_splits

# NB: figure out why these functions work
# bp = {"Y": 1.0, "X": 0.39257861423974655, "Yaw": -1.6499993, "Z": -0.2203967099795332,"Pitch": 46.499996}
# coord_test = get_perspective_coord_repr(bp)
# print(coord_test)


current_folder=os.getcwd()

open_path = '/home/kate/minecraft_corpus/snippets/snippets_out/'
contents = os.listdir(open_path) 
# snip_file = contents[0]
#snip_file = '2023-06-09_1_snippets.json'
snip_file = '2023-06-29_256_snippets.json'

json_files = os.listdir(open_path)

json_save_path = '/home/kate/cocobots_minecraft/neural_builder_data/'

if not os.path.isdir(json_save_path):
    os.makedirs(json_save_path)

observation_path = '/home/kate/cocobots_minecraft/observation_logs/'
observation_files = os.listdir(observation_path)

data = []
final_snippet_split = []
done_count = 0
passed = 0
with open(open_path + snip_file, 'r') as jf:
    jfile = json.load(jf)
    for game in jfile:
    #for game in [g for g in jfile if g['id'] == 'C106-B37-A23']:
        game_list = []#use this to store each snippet in order
        game_id = game['id']
        final_snippet_split.append(game_id.split('-')[0]) 
        #get the observation files
        experiment_id = None
        for o in observation_files:
            if game_id in o:
                experiment_id = o
                break
        with open(observation_path + experiment_id, 'r') as obs_json:
            logs = json.load(obs_json)
            worldstates = logs['WorldStates']
            print('Log file opened')
        for snippet in [item[1] for item in game.items() if item[0] != 'id']:
            data_point = {}
            #JSON ID (**OURS)
            data_point['json_id'] = game['id']
            #ORIG EXPERIMENTAL ID 
            data_point['orig_experiment_id'] = logs['orig_experimental_id'].split('/')[-1]
            snip = []
            for s in snippet:
                speaker = s['Speaker']
                text = s['text'].strip()
                if speaker == 'System':
                    #NEXT BUILDER ACTIONS
                    data_point['next_builder_actions'] = get_next_builder_actions(text)
                    # print(data_point['next_builder_actions'])
                    break # stop the loop here since we don't care about moves that are after builder moves
                else:
                    #toks = wordpunct_tokenize(text)
                    toks = tokenize(text)[0]
                    if 'Arch' in speaker:
                        new_speaker = 'Architect'
                    else:
                        new_speaker = 'Builder'
                    # print(new_speaker)
                    # print(toks)
                    snip.append((new_speaker, toks))
            data_point['utt_snips'] = snip #this is temporary to get correct match with log file
            #PREVIOUS UTTERANCES
            #TBD
            # data_point['prev_utterances'] = get_instruction(snip)
            game_list.append(data_point)
        print(done_count)
        done_count += 1
        print('{} snippets in {}'.format(len(game_list), game_id))
        #return observation data
        #open correct log file using game id
        #for each turn in the file, find the one which corresponds to 
        wi=0
        for dp in game_list:
            # print(dp)
            last_speaker = dp['utt_snips'][-1][0]
            last_utt_toks = dp['utt_snips'][-1][1]
            # last_speaker = dp['prev_utterances'][-1]['speaker']
            #last_utt_toks = dp['prev_utterances'][-1]['utterance']
            # print(last_speaker)
            # print(last_utt_toks)

            i, bpos, pconf = return_state_info(worldstates, last_speaker, last_utt_toks, wi)
            if bpos == None:
                #probably because couldn't match the speaker
                passed += 1
                pass

            else:
                # print('index: {}'.format(i))
                # print(bpos)
                wi = i + 1 
                # #SAMPLE ID 
                # #PREVIOUS BUILDER POSITION
                # #PREVIOUS CONFIG
                dp['sample_id'] = i + 1 #need to add 1 to match with original BAP sample id
                # dp['from_aug_data'] = False
                # dp['prev_builder_position'] = bpos
                # dp['prev_config'] = pconf
                # #BUILT CONFIG
                # bconf = get_built_config(dp['prev_config'], dp['next_builder_actions'])
                # dp['built_config'] = bconf

                # #PERSPECTIVE COORDINATES
                # dp['perspective_coordinates'] = torch.tensor(get_perspective_coord_repr(bpos))

                data.append(dp)

print('{} snippets passed'.format(str(passed)))
##RETURN JSON OF SNIPPETS TO KEEP
snippets = defaultdict(list)
# final_snippets = []

for snip in data:
    snippets[snip['orig_experiment_id']].append(snip['sample_id'])
final_snippets = {k:v for k,v in snippets.items()}
# for k,v in snippets.items():
#     final_snippets[k] = v
#     json_format = {}
#     json_format['orig_experiment_id'] = k
#     json_format['sample_ids'] = v
#     final_snippets.append(json_format)


# RETURN NEW SPLITS
with open(current_folder + '/orig_splits.json', 'r') as s:
    splitjson = json.load(s)
    new_splits = get_splits(splitjson, final_snippet_split)

with open(current_folder + '/new_splits.json', 'w') as outfile:
    json.dump(new_splits, outfile)
print('new splits json saved')
print('new splits: {} train, {} val, {} test'.format(len(new_splits['train']), len(new_splits['val']), len(new_splits['test'])))
print('----------------------------')

##this below was to check the output
# print_list = []
# for d in data:
#     for item in d.items():
#         if item[0] not in ['perspective_coordinates', 'json_id', 'orig_experiment_id', 'from_aug_data', 'prev_config', 'built_config']:
#             if item[0] == 'sample_id':
#                 print_list.append('---SAMPLE id: {} ***----'.format(str(item[1])))
#             elif item[0] == 'next_builder_actions':
#                 print_list.append('next builder actions:')
#                 for move in item[1]:
#                     pp = move.get_action()
#                     coord = move.get_coords()
#                     print_list.append(pp + ' ' + coord[0] + ' ' + coord[1] + ' ' + coord[2] + ' ' + coord[3])
#                     print_list.append('---------------')
#             else:
#                 print_list.append(item[0])
#                 print_list.append(str(item[1]))

#     print_list.append('-------------------------------------------------------------')

# print_string = '\n'.join(print_list)
# with open (current_folder + '/' + 'C154-B29-A1' + '-bap.txt', 'w') as txt_file:
#     txt_file.write(print_string)
    
#save json
now = datetime.datetime.now().strftime("%Y-%m-%d")

with open(current_folder  + '/snippets_' + now + '.json', 'w') as outfile:
    json.dump(final_snippets, outfile)

print('json saved')

  
            
       
                        
