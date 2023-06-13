"""
for each snippet, run functions to return a list of datapoints 
which are formatted according to 
https://github.com/prashant-jayan21/minecraft-bap-models/blob/master/docs/data_format.md

fields:
builder_action_history [empty for now]
next_builder_actions
prev_utterances
gold_config [ignore for now??]
built_config
prev_config
prev_builder_position
perspective_coordinates **
from_aug_data [always 0]
json_id [??]
sample_id
orig_experiment_id [???]

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

save_path = current_folder + '/json_flat/'

json_files = os.listdir(open_path)

json_save_path = '?'

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
        for o in observation_files:
            if game_id in o:
                print(game_id)
                print(o)
                with open(observation_path + o, 'r') as obs_json:
                    logs = json.load(obs_json)
                    worldstates = logs['WorldStates']
                print('Log file opened')
        for snippet in [item[1] for item in game.items() if item[0] != 'id']:
            data_point = {}
            snip = []
            for s in snippet:
                speaker = s['Speaker']
                text = s['text'].strip()
                if speaker == 'System':
                    #FIELD 1
                    data_point['next_builder_actions'] = get_next_builder_actions(text)
                    break # stop the loop here since we don't care about moves that are after builder moves
                else:
                    toks = wordpunct_tokenize(text)
                    if 'Arch' in speaker:
                        new_speaker = 'Architect'
                    else:
                        new_speaker = 'Builder'
                    snip.append((new_speaker, toks))
            #FIELD 2
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
            print(last_speaker)
            print(last_utt_toks)
            # print(dp['next_builder_actions'])
            i, bpos, pconf = return_state_info(worldstates, last_speaker, last_utt_toks, wi)
            wi = i
            #FIELDS 3 - 5
            dp['sample_id'] = i
            dp['prev_builder_position'] = bpos
            dp['prev_config'] = pconf

        #then calculate built config
        #FIELDS 6 - 
        for dp in game_list:
            bconf = get_built_config(dp['prev_config'], dp['next_builder_actions'])
            dp['built_config'] = bconf
            
            #then calculate perspective coordinates


            print('-------------------------------------------')

            
       
                        
