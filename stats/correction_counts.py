import os
import json
# from collections import defaultdict


current_folder=os.getcwd()

corpus_path = current_folder + '/jsons/TEST_100_bert.json'

print_list = []

with open(corpus_path, 'r') as j:
    jfile = json.load(j)
    games = jfile
    all_corrections = []
    no_corrs = 0
    total_games = len(games)
    for game in games:
        game_list = []
        
        corr_count = len([r for r in game['relations'] if r['type'] == 'Correction'])
        
        if corr_count > 0:
            game_list.append(game['id'])
            game_list.append(corr_count)
            all_corrections.append(game_list)
        else:
            no_corrs += 1

#order the games with most corrections to least
all_corrections.sort(key=lambda x: x[1])

print_string = ''
for corr in all_corrections:
    s =  corr[0] + ' : ' + str(corr[1]) + ' corrections' + '\n'
    print_string += s

# print_string = '\n'.join(all_corrections)
    

with open (current_folder+ '/test_corrections.txt', 'w') as txt_file:
    txt_file.write(print_string)

print('corrections saved')

print('{} games out of {} have no corrections.'.format(no_corrs, total_games))

