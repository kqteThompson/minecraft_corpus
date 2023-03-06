'''
input: a squished data json with predicted relations 
output: a text file
NB: this is a test to see if squished can be represented in glozz format
'''
import os
import json


input_json = 'bert_pred.json'

current_folder=os.getcwd()

data_path = current_folder + '/' + input_json

save_path= current_folder + '/texts/'
if not os.path.isdir(save_path):
    os.makedirs(save_path)

with open(data_path, 'r') as jf:
    games = json.load(jf)

for game in games:
    text_list = [] 
    last_speaker = game['edus'][0]['speaker']
    game_id = game['id']
    print(game_id)
    text_list.append(game_id)

    sents = []
    for edu in game['edus']:
        if edu['speaker'] == last_speaker:
            sents.append(edu['text'])
        else:
            utterance = '<'+ last_speaker + '>'
            #put '&' between all sentences
            #IF speaker is not 'System'
            if last_speaker != 'System':
                for s in sents:
                    utterance += ' ' + s + ' &'
                utterance = utterance.strip('&')
            else:
                for s in sents:
                    utterance += ' ' + s 
            text_list.append(utterance)
            sents = []
            last_speaker = edu['speaker']
            sents.append(edu['text'])
    if len(sents) > 0:
        utterance = '<'+ edu['speaker'] + '>'
        for s in sents:
            utterance += ' ' + s
        text_list.append(utterance)
    
    game_string = '\n'.join(text_list)

    with open (save_path + '/' + game_id + '.txt', 'w') as text_file:
        text_file.write(game_string)


