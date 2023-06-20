"""
for each snippet, run functions to return a list of datapoints 
which are formatted according to 
https://github.com/prashant-jayan21/minecraft-bap-models/blob/master/docs/data_format.md

fields:
1. builder_action_history [TODO] [list of builder actions objects]
2. next_builder_actions [TODO] [builder action objects]

3. prev_utterances [TODO] all previous utterances including moves
NB: first one is  always:  utterance': ['<dialogue>']
{'speaker': 'Builder', 'utterance': ['<builder_putdown_orange>']}, 
{'speaker': 'Builder', 'utterance': ['<builder_putdown_orange>']}, 
{'speaker': 'Builder', 'utterance': ['<builder_pickup_orange>']}, 
{'speaker': 'Architect', 
'utterance': ['build', 'one', 'orange', 'on', 'top', 'of', 'it']}, 
{'speaker': 'Builder', 'utterance': ['<builder_putdown_orange>']}...

4. gold_config [ignore for now??]
<DrawBlock type="cwcmod:cwc_minecraft_green_rn" x="95" y="1" z="100"/>

5. built_config [NB: take out absolute coordinates fields] 
eg: [{'x': 0, 'y': 1, 'z': -5, 'type': 'yellow'}, 
{'x': 0, 'y': 2, 'z': -4, 'type': 'yellow'}, 
{'x': 0, 'y': 3, 'z': -3, 'type': 'yellow'}, 
{'x': -3, 'y': 1, 'z': -1, 'type': 'orange'}, 
{'x': -3, 'y': 2, 'z': -1, 'type': 'orange'}]
BUT SHOULD IT LOOK LIKE THIS
{'Y': 1, 'X': 4, 'Z': 0, 'Type': 'cwc_minecraft_red_rn'}, 

6. prev_config 
7. prev_builder_position
8. perspective_coordinates
9. from_aug_data (always 0) 
10. json_id [TODO]
11. sample_id 
12. orig_experiment_id [TODO] 
ex
orig_experiment_id
B1-A4-C54-1522773776201

"""
import os 
import json 
import datetime
import numpy as np
import torch
import nltk
# from nltk.tokenize import wordpunct_tokenize
from world_state import get_next_builder_actions, get_instruction, return_state_info, get_built_config
from prashant import get_perspective_coord_repr, tokenize
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
snip_file = '2023-06-19_162_snippets.json'

json_files = os.listdir(open_path)

json_save_path = '/home/kate/cocobots_minecraft/neural_builder_data/'

if not os.path.isdir(json_save_path):
    os.makedirs(json_save_path)

observation_path = '/home/kate/cocobots_minecraft/observation_logs/'
observation_files = os.listdir(observation_path)

data = []
final_snippet_split = []
done_count = 0
with open(open_path + snip_file, 'r') as jf:
    jfile = json.load(jf)
    for game in jfile:
    # for game in [g for g in jfile if g['id'] == 'C32-B53-A15']:
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
            # last_utt_toks = dp['prev_utterances'][-1]['utterance']
            # print(last_speaker)
            # print(last_utt_toks)
            # print('-----OUTER CIRCLE------')
            i, bpos, pconf = return_state_info(worldstates, last_speaker, last_utt_toks, wi)
            # print('index: {}'.format(i))
            # print(bpos)
            wi = i + 1
            # #SAMPLE ID 
            # #PREVIOUS BUILDER POSITION
            # #PREVIOUS CONFIG
            dp['sample_id'] = i
            dp['from_aug_data'] = False
            dp['prev_builder_position'] = bpos
            dp['prev_config'] = pconf
            #BUILT CONFIG
            bconf = get_built_config(dp['prev_config'], dp['next_builder_actions'])
            dp['built_config'] = bconf

            #PERSPECTIVE COORDINATES
            dp['perspective_coordinates'] = torch.tensor(get_perspective_coord_repr(bpos))

            data.append(dp)


# # RETURN NEW SPLITS
# with open(current_folder + '/orig_splits.json', 'r') as s:
#     splitjson = json.load(s)
#     new_splits = get_splits(splitjson, final_snippet_split)

# with open(current_folder + '/new_splits.json', 'w') as outfile:
#     json.dump(new_splits, outfile)
# print('new splits json saved')
# print('new splits: {} train, {} val, {} test'.format(len(new_splits['train']), len(new_splits['val']), len(new_splits['test'])))
# print('----------------------------')


for item in data[0].items():
    if item[0] != 'perspective_coordinates':
        print(item[0])
        print(item[1])
        print('---------------------------------')

##save json
# now = datetime.datetime.now().strftime("%Y-%m-%d")

# with open(json_save_path + snip_file.strip('.json') + '_' + now + '.json', 'w') as outfile:
#     json.dump(data, outfile)

# print('json saved')

  
            
       
                        
