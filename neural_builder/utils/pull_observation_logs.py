import os
import json
import nltk 
from nltk.tokenize import wordpunct_tokenize
# from collections import defaultdict

"""
navigates through the observation logs files provided by Hockenmeier team
for each one, saves a new copy with less data
which will be matched up with our snippets. 
Final logs will include:
-timestamp
-builder postion
-blocks in grid
-chat -- NB: if it's the first time an utterance is made, then it is stored as 'first chat'.
However, if the game moves continue and no new utterances are made, then the same utterance
is stored as 'chat continued', until the next new utterance is made.
"""

current_folder=os.getcwd()

original_corpus_path = '/home/kate/minecraft/corpus_small/'

folder_array = os.listdir(original_corpus_path) 

#json_save_path = current_folder + '/observations_short/'
json_save_path = '/home/kate/cocobots_minecraft/observation_logs/'

if not os.path.isdir(json_save_path):
    os.makedirs(json_save_path)

for folder in folder_array:
    if os.path.isdir(original_corpus_path + folder):
        date_dir = os.listdir(original_corpus_path + folder + '/logs')
        # print(folder)
        # print(date_dir)
        for dir in [d for d in date_dir if d !='.DS_Store']:
            name = dir.split('-')
            new_name = name[2] + '-' + name[0] + '-' + name[1] + folder.split('data')[1]
            ##open the json and edit
            with open(original_corpus_path + folder + '/logs/' + dir + '/postprocessed-observations.json', 'r') as jf:
                jfile = json.load(jf)
                states = jfile['WorldStates']
                new_world = []
                last_chat = []
                last_utterance = []
                index = 0
                for state in states:
                    new_state = {}
                    new_state['state_index'] = index
                    index += 1
                    new_state['BuilderPosition'] = state['BuilderPosition']
                    new_state['Timestamp'] = state['Timestamp']
                    new_state['BlocksInGrid'] = state['BlocksInGrid']
                    #keep only the new utterances
                    new_utt = [u for u in state['ChatHistory'] if u not in last_chat]
                    if len(new_utt) == 0:
                        new_utt = last_utterance
                        new_state['chat_continued'] = new_utt
                    else:
                        last_chat = state['ChatHistory']
                        last_utterance = new_utt
                        fchat = {}
                        fchat['utterance'] = new_utt
                        tokens = []
                        for utt in new_utt:
                            if '<Arch' in utt:
                                t = ['Architect', wordpunct_tokenize(utt.split('>')[1])]
                            else:
                                t = ['Builder', wordpunct_tokenize(utt.split('>')[1])]
                            tokens.append(t)
                        fchat['tokens'] = tokens
                        new_state['first_chat'] = fchat
                    #save old history
                    new_world.append(new_state)
                #replace worlstates field with new world
                jfile['WorldStates'] = new_world
                jfile['orig_experimental_id'] = folder + '/logs/' + dir

            with open(json_save_path + new_name + '_' + 'observations' + '.json', 'w') as outfile:
                json.dump(jfile, outfile)

            print('{} json saved'.format(new_name))




