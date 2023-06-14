"""
for each snippet, run functions to return a list of datapoints 
which are formatted according to 
https://github.com/prashant-jayan21/minecraft-bap-models/blob/master/docs/data_format.md

fields:
1. builder_action_history [TODO]
2. next_builder_actions
3. prev_utterances [**DO WE NEED TO ADD ALL?] [TODO]
4. gold_config [ignore for now??]
5. built_config 
6. prev_config
7. prev_builder_position
8. perspective_coordinates [TODO]
9. from_aug_data (always 0) 
10. json_id [TODO]
11. sample_id 
12. orig_experiment_id [TODO]

"""
import os 
import json 
import datetime
import nltk
from nltk.tokenize import wordpunct_tokenize
from world_state import get_next_builder_actions, get_instruction, return_state_info, get_built_config

current_folder=os.getcwd()

open_path = '/home/kate/minecraft_corpus/snippets/snippets_out/'
contents = os.listdir(open_path) 
# snip_file = contents[0]
snip_file = '2023-06-09_1_snippets.json'

json_files = os.listdir(open_path)

json_save_path = '/home/kate/cocobots_minecraft/neural_builder_data/'

if not os.path.isdir(json_save_path):
    os.makedirs(json_save_path)

observation_path = '/home/kate/cocobots_minecraft/observation_logs/'
observation_files = os.listdir(observation_path)

data = []
with open(open_path + snip_file, 'r') as jf:
    jfile = json.load(jf)
    for game in jfile:
        game_list = []#use this to store each snippet in order
        game_id = game['id']
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
            #ORIG EXPERIMENTAL ID (*ours)
            data_point['orig_experiment_id'] = experiment_id
            snip = []
            for s in snippet:
                speaker = s['Speaker']
                text = s['text'].strip()
                if speaker == 'System':
                    #NEXT BUILDER ACTIONS
                    data_point['next_builder_actions'] = get_next_builder_actions(text)
                    break # stop the loop here since we don't care about moves that are after builder moves
                else:
                    toks = wordpunct_tokenize(text)
                    if 'Arch' in speaker:
                        new_speaker = 'Architect'
                    else:
                        new_speaker = 'Builder'
                    snip.append((new_speaker, toks))
            #PREVIOUS UTTERANCES
            data_point['prev_utterances'] = get_instruction(snip)
            game_list.append(data_point)
        print('{} snippets in {}'.format(len(game_list), game_id))
        #return observation data
        #open correct log file using game id
        #for each turn in the file, find the one which corresponds to 
        wi=0
        for dp in game_list:
            last_speaker = dp['prev_utterances'][-1]['speaker']
            last_utt_toks = dp['prev_utterances'][-1]['utterance']
            # print(last_speaker)
            # print(last_utt_toks)
            # print(dp['next_builder_actions'])
            i, bpos, pconf = return_state_info(worldstates, last_speaker, last_utt_toks, wi)
            wi = i
            #SAMPLE ID 
            #PREVIOUS BUILDER POSITION
            #PREVIOUS CONFIG
            dp['sample_id'] = i
            dp['from_aug_data'] = 0
            dp['prev_builder_position'] = bpos
            dp['prev_config'] = pconf
            #BUILT CONFIG
            bconf = get_built_config(dp['prev_config'], dp['next_builder_actions'])
            dp['built_config'] = bconf

            data.append(dp)

            # print('-------BUILDER ACTIONS-----')
            # print(dp['next_builder_actions'])
            # print('-------PREV CONFIG-----')
            # print(dp['prev_config'])
            # print(['---final config-----'])
            
            # print(dp['built_config'])
            # print('==============================================================')


##save json
now = datetime.datetime.now().strftime("%Y-%m-%d")

with open(json_save_path + snip_file.strip('.json') + '_' + now + '.json', 'w') as outfile:
    json.dump(data, outfile)

print('json saved')

  
            
       
                        
