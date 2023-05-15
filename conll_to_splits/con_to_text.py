'''
input: a single conll output from segementer
output: folder with txt files with apersand edu separators

for line in text 
step 1: if of format #B16-A41-C24-1522945785686-- record as game number
step 2: if <builder>/<architect> then start new turn
    step 2.1: for sent -- if not last sent, add &
    step 1.2: within sent -- for line in sent, first word is word
    and last word if BeginSeg=Yes, then add &
step 3: if [asdfsdf] then this is just system moves and goes on a new line.

see if you can get a split list
then for each one create an object that will then be turned into a txt file.
'''

import os

current_folder=os.getcwd()

save_path= current_folder + '/conll_text/'
if not os.path.isdir(save_path):
    os.makedirs(save_path)

conll_path = current_folder + '/minecraft_predict.conll'


def remove_contractions(turn):
    if '\'s' in turn:
        while '\'s' in turn:
            i = turn.index('\'s')
            turn[i-1] = turn[i-1]+'\'s' 
            del(turn[i])
    if 'n\'t' in turn:
        print('yep')
        while 'n\'t' in turn:
            i = turn.index('n\'t')
            turn[i-1] = turn[i-1]+'n\'t' 
            del(turn[i])
    if '\'re' in turn:
        print('yep')
        while '\'re' in turn:
            i = turn.index('\'re')
            turn[i-1] = turn[i-1]+'\'re' 
            del(turn[i])
    return turn

with open(conll_path, 'r') as txt:
    text = txt.read().split('\n\n')

    all_games = []
    game_no = None
    game_list = []
    text_string = []
    speaker = None
    for t in text:
        for i in t.split('\n'):
            print(i)
            if i.startswith('#B'):
                #save previous game
                if len(game_list) > 1:
                    if len(text_string) > 1:
                        del(text_string[1])
                        game_list.append(text_string)
                    all_games.append(game_list)
                    game_list = []
                    text_string = []
                    speaker = None
                game_no = i.lstrip('#')
                game_list.append(game_no) 
                continue
            if i.startswith('#[Builder'):
                if len(text_string) > 1:
                    del(text_string[1])
                    game_list.append(text_string)
                    text_string = []
                    speaker = None
                game_list.append(i.lstrip('#'))
                continue
            if i.startswith('#<Builder'):
                if speaker != '<Builder>':
                    if len(text_string) > 1:
                        del(text_string[1])
                        game_list.append(text_string)
                    text_string = []
                    text_string.append('<Builder>')
                    speaker = '<Builder>'
                continue
            if i.startswith('#<Arch'): 
                if speaker != '<Architect>':
                    if len(text_string) > 1:
                        del(text_string[1])
                        game_list.append(text_string)
                    text_string = []
                    text_string.append('<Architect>')
                    speaker = '<Architect>'
                continue
            try:
                if i[0].isdigit():
                    l = i.split('\t')
                    if l[-1] == 'BeginSeg=Yes':
                        text_string.append('&')
                        text_string.append(l[1])
                    else:
                        text_string.append(l[1])
            except IndexError:
                continue
    if len(text_string) > 1:
        del(text_string[1])
        game_list.append(text_string)
    all_games.append(game_list)
    print('done with game list: {} games.'.format(len(all_games)))

    for game in all_games:
        game_number = game[0].split('-')
        new_list = []
        for line in game:
            if type(line) == list:
                line = remove_contractions(line)
                new_line = ' '.join(line).strip()
                new_list.append(new_line)
            else:
                new_list.append(line)
        new_game = '\n'.join(new_list)

        save_name = game_number[2] + '-' + game_number[0] + '-' + game_number[1] + '_data'

        with open (save_path + '/' + save_name + '.txt', 'w') as txt_file:
            txt_file.write(new_game)
            print('game {} done'.format(save_name))
