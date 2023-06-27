import os
import pickle 
from utils import *

current_folder=os.getcwd()

open_path = current_folder + '/pickles/save_B29-A1-C154_sample_snips.pkl'

print(open_path)

with open(open_path, 'rb') as handle:
    bap_data = pickle.load(handle)

print('opened!')
print(len(bap_data))


# test_elem = bap_data[-1]['prev_utterances']
# for elem in test_elem:
#     print(elem)


# pr = bap_data[13]['prev_config']
# test_elem = bap_data[13]['builder_action_history']
# test_elem_list = bap_data[13]['next_builder_actions']
# for elem in test_elem_list:
#     print('len action history {}'.format((elem.get_action().print())))
#     print('len action history {}'.format(len(elem.get_action_history())))
#     print('len built config {}'.format(len(elem.get_built_config())))
#     print('len prev config {}'.format(len(elem.get_prev_config())))
#     print('--------------------------------')

sample_ids = [16, 22, 27, 36, 66, 70, 89, 130, 139]
text_list = []
snip_num = 0
prev_utts = 0

for element in bap_data:
    print(element['sample_id'])
    if element['sample_id'] in sample_ids:
        text_list.append('--------------------- INSTRUCTION ' + str(snip_num) + '------')
        text_list.append('sample_id : ' + str(element['sample_id']))
        snip_num+= 1
        utts = element['prev_utterances'][prev_utts:]
        for utt in utts:
            words = ' '.join(utt['utterance'])
            text_list.append(utt['speaker'] + ' : ' + words)
        prev_utts = len(element['prev_utterances'])
        text_list.append('--------MOVES--------')
        actions = element['next_builder_actions']
        
        for action in actions:
            text_list.append('--------------')
            pp = action.get_action().get_action()
            coord = action.get_action().get_coords()
            text_list.append(pp + ' ' + coord[0] + ' ' + coord[1] + ' ' + coord[2] + ' ' + coord[3])
        
        text_list.append('json_id : ' + str(element['json_id']))
        text_list.append('prev_builder_position : ' + str(element['prev_builder_position']))
        text_list.append('--------------------------------------------------------------')

print_string = '\n'.join(text_list)
    
with open (current_folder + '/' + 'original_data_samples' + '-bap.txt', 'w') as txt_file:
    txt_file.write(print_string)







