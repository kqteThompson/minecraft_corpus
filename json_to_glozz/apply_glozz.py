'''
input: json files in json folder
output: folder with .aa files to be read by glozz
'''
import os
import json
from glozz_format import get_format


current_folder=os.getcwd()

aa_path = current_folder + '/aa_files/'

json_path= current_folder + '/json/'

json_files = os.listdir(json_path)

for f in json_files:
    with open(json_path + f, 'r') as jf:
        jfile = json.load(jf)
        for game in jfile:
            print(game['game_id'])
            game_name = game['game_id'] + '_flattened'
            aa_file = get_format(game)
            with open (aa_path + game_name + '.aa', 'w') as xml_file:
                xml_file.write(aa_file)
     
        print('Game {} done'.format(game_name))


