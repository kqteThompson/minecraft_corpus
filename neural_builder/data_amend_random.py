"""
Takes a json of games and sample ids to remove from the BAP data 
returns an amended data set to run anyway
snippets = {game_id : [list of sample ids to keep]}

len of train data 4453
1082 samples skipped
161 games replaces with our snippets

"""
import os
import pickle
import random
from utils import BuilderAction


current_folder=os.getcwd()

#open train_data
data_open = current_folder + '/generated_data/train-samples.pkl'

save_file = current_folder + '/generated_data/random-train-samples.pkl'

with open(data_open, 'rb') as handle:
    bap_data = pickle.load(handle)

new_bap = []
bap_indices = [i for i in range(len(bap_data))]
random_drop = random.sample(bap_indices, 1735)
new_bap = [s for i,s in enumerate(bap_data) if i not in random_drop]

    
print('{} samples dropped'.format(len(random_drop)))
print('len of new random training data {}'.format(len(new_bap)))

#save new data
with open(save_file, 'wb') as f:
    pickle.dump(new_bap, f, protocol=3)