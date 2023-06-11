import os
import json
# from collections import defaultdict


current_folder=os.getcwd()

corpus_path = '/home/kate/cocobots_minecraft/splits'

folder_array = os.listdir(corpus_path) 

matchups_list = []
split = None
for folder in folder_array:
    split = folder
    game_list = os.listdir(corpus_path + '/' + folder)
    for game_file in game_list:
        l = split + '   ' + game_file.split('_')[0] + '   ' + game_file.split('data-')[1].strip('.txt')
        matchups_list.append(l)

print_string = '\n'.join(matchups_list)
with open (current_folder+ '/game_date.txt', 'w') as txt_file:
            txt_file.write(print_string)


