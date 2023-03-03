"""
Takes a json file of bert formatted games and returns a json ready for BERT 
in which consecutive System moves are combined in a single edu
!!NB this is a throwaway script because it doesn't take into account labeled data 
WIP figure out what do do about the relations in this case.
"""
import os 
import json 
import re
import datetime

def text_replace(text):
    colors  = ['red', 'blue', 'green', 'orange', 'yellow', 'purple', 'black']
    color = re.findall(r"\b({})\b".format('|'.join(colors)), text, flags=re.IGNORECASE)
    if 'puts' in text:
        replacement = 'puts down a {} block.'.format(color[0])
    else:
        replacement = 'picks up a {} block.'.format(color[0])
    return replacement

current_folder=os.getcwd()

open_path = current_folder + '/json_out/'  #!takes already flattened without name changes games!

save_path= current_folder + '/json_squished_out/'

json_files = os.listdir(open_path)

builder_names_replace = 1
with_relations = 0
split = 'dev'
annotation_level = 'BRONZE'

output_list = []

for f in json_files:
    with open(open_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            last_system = []
            new_game_edus = []
            for edu in game['edus']:
                if edu['speaker'] == 'System':
                    new_text = text_replace(edu['text'])
                    last_system.append(new_text)
                else:
                    if len(last_system) > 0:
                        #append all previous system moves
                        squish = ' '.join(last_system)
                        squish_edu = {}
                        squish_edu['text'] = squish
                        if builder_names_replace:
                            squish_edu['speaker'] = 'Builder'
                        else:
                            squish_edu['speaker'] = 'System'
                        new_game_edus.append(squish_edu)
                        #clear list
                        last_system = []
                    new_game_edus.append(edu)
                    
                    
            if len(last_system) > 0:
                #just in case there's anything left in last system.
                squish = ' '.join(last_system)
                squish_edu = {}
                squish_edu['text'] = squish
                if builder_names_replace:
                    squish_edu['speaker'] = 'Builder'
                else:
                    squish_edu['speaker'] = 'System'
                new_game_edus.append(squish_edu)

            game['edus'] = new_game_edus
            output_list.append(game)

print('{} {} games formatted.'.format(len(output_list), split))    

now = datetime.datetime.now().strftime("%Y-%m-%d")

##save bert json
save_file_name = save_path + now + annotation_level + '_' + split + '_'+ str(len(output_list)) +'_bert_squished.json'

with open(save_file_name, 'w') as outfile:
    json.dump(output_list, outfile)

print('json saved')