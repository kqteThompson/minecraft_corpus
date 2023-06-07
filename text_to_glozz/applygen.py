'''
input: folder of folders organized by date each containing dialogue-with-actions.txt file with dialogues
output: folder with .aa and .ac files for glozz annotation
'''
import os
from genglozzsegments import get_format
# from gensquishglozz import get_format


current_folder=os.getcwd()

corpus_path = '/home/kate/minecraft_corpus/conll_to_splits/conll_text/'
#corpus_path = '/home/kate/cocobots_minecraft/splits_reseg/test_all_reseg/'

save_path= current_folder + '/glozz_train/'
if not os.path.isdir(save_path):
    os.makedirs(save_path)

folder_array = os.listdir(corpus_path) 

for f in folder_array:
    # print(corpus_path + f)
    # if f in ['C33-B47-A30_data-4-12.txt']: 
    with open(corpus_path + f, 'r') as txt:
        text = txt.readlines()
        dialogue = []
        for line in text:
            dialogue.append(line.strip('\n'))

        ac_file, aa_file, dialogue_id = get_format(dialogue)
        with open (save_path + '/' + dialogue_id + '.aa', 'w') as xml_file:
            xml_file.write(aa_file)
        with open (save_path + '/' + dialogue_id + '.ac', 'w') as text_file:
            text_file.write(ac_file)
        print('dialogue done', dialogue_id)

                    
            
               