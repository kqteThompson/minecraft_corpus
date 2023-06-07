import os
from collections import defaultdict


train_done = ['C3', 'C17', 'C32', 'C63', 'C64', 'C59', 
              'C57', 'C18', 'C149', 'C80', 'C72', 'C154', 'C31', 
              'C90', 'C47', 'C93', 'C22', 'C75', 'C120']


current_folder=os.getcwd()

corpus_path = '/home/kate/minecraft_corpus/conll_to_splits/conll_text/'

folder_array = os.listdir(corpus_path) 

val_dict = defaultdict(int)
total_count = 0

print_list = []

for f in folder_array:
    n = f.split('_')[0]
    if n.split('-')[0] not in train_done:
        #find length 
        with open(corpus_path + f, 'r') as txt:
            text = txt.readlines()
            text_len = len(text)
        
        print_list.append((n, text_len))

    # if f.split('-')[0] in val:
    #     val_dict[f.split('-')[0]] += 1
    #     total_count += 1
    # print(corpus_path + f)
    # if f in ['C33-B47-A30_data-4-12.txt']: 

print('{} games left'.format(len(print_list)))

#order list 
print_list.sort(key = lambda x: x[1])
sorted_list = []
for p in print_list:
    #print(p[0], p[1])
    sorted_list.append(p[0] +' has len: ' + str(p[1]))

print_string = '\n'.join(sorted_list)
with open (current_folder+ '/trainset.txt', 'w') as txt_file:
            txt_file.write(print_string)

