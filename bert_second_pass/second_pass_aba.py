"""
Takes output from second_pass.py and outputs a list of candidates, labels and raw text
for bert linear that considers only arch cans that have a non linguistic move between them. 

"""
import os 
import json 
import pickle
from collections import defaultdict, Counter

current_folder=os.getcwd()

open_path = current_folder + '/json_out/'
save_path = current_folder + '/pickle_out/'


games = 'TRAIN_314_bert_2p1.json'

games_save = 'TRAIN_314_bert_2p1.pck'


final_candidates =  []

#for each game, get a list of turn no's after which there is a builder move
#then for edu in edu, if turn in list, then for every edu in that turn, make a candiate with every 
#other edu in all architect turns after.

def get_turns(edus):
    """takes a list of edus from one game and returns
    a dict of architect turns that will require skipping when forming candidates
    """
    turns = []
    last = 0
    for g in edus:
        if g['speaker'] == 'Architect':
            if g['turn'] != last:
                turns.append(g['turn'])
                last = g['turn']
        elif g['type'] == 0:
            turns.append('NL')
    # #NB:  gives us a list like this:
    # # [2, 4, 'NL', 6, 'NL', 8, 'NL', 10, 12, 13, 14, 'NL', 15, 'NL', 16, 'NL', 18, 'NL']
    # #will create a dict below like so: {2: [4], 10: [12, 13, 14], 12: [13, 14], 13: [14]}

    # print(turns)
    turn_dict = defaultdict(list)
    for i, t in enumerate(turns):
        if t != 'NL':
            n = 1
            try:
                while turns[i+n] != 'NL':
                    turn_dict[t].append(turns[i+n]) 
                    n+=1
            except IndexError:
                # print(t)
                #NB: this is because it hits the end of the list
                continue
    return turn_dict

def format_preds(preds_file):
    """
    if bert output, need to change relations field
    """
    for game in preds_file:
        new_rels = []
        rels = game['pred_relations']
        for rel in rels:
            rel['x'] = int(rel['x'])
            rel['y'] = int(rel['y'])
            new_rels.append(rel)
        game['relations'] = new_rels
    return preds_file

MAX_LEN = 16

with open(open_path + games, 'r') as jf:
    jfile = json.load(jf)
    if 'preds' in games:
        jfile = format_preds(jfile)
    

    labels = []
    raw = []
    input_text = []

    for game_ind, game in enumerate(jfile):

        # if game['id'] == 'C58-B1-A44':

        raw_text = [j["speaker"][:5] + ": " + j["text"] for j in jfile[game_ind]["edus"] ]
        raw += [raw_text]

        #make raw text 

        #get candidates
        game_cands = []
        edus = game['edus']
        turns = get_turns(edus)
        #dict of turns to avoid
        # print(turns)

        ##get edu list
        archs = [t for t in edus if t['speaker'] != 'Builder' and t['turn_ind'] <= 3]

        ##make relations list for easy access during candidate production.
        rels = [(r['x'], r['y']) for r in game['relations']]
        # print(rels)

        for edu in archs:
            num = edu['turn']
            avoid = []
            #then this will be source
            if edu['turn'] in turns.keys():
                avoid = turns[edu['turn']]
            for target in [elem for elem in archs if elem['turn'] > num and elem['turn'] not in avoid]:
                cand = [game_ind, edu['global_index'], target['global_index'], 0, -1, edu['res'], edu['res']]
                if (cand[1], cand[2]) in rels:
                    cand[3] = 1
                    cand[4] = 14
                game_cands.append(cand)
        # print(game_cands)

        #reduce cands to those under specified cutoff
        if MAX_LEN:
            game_cands = [c for c in game_cands if abs(c[2] - c[1]) <= MAX_LEN]
        # for ca in game_cands:
        #     print(ca[2] - ca[1])
        
        #create input text pairs from candidates
    
        text = [[raw_text[cand[1]], raw_text[cand[2]]] for cand in game_cands]
        
        
        labels.extend(game_cands)
        input_text.extend(text)

        print('Game {} has length {} and  has {} candidates'.format(game['id'], len(raw_text), len(game_cands)))

    # use this to see the distance distributions
    # distances = [abs(i[2] - i[1]) for i in labels if i[3] == 1]
    # dist_cnts = Counter(distances)
    # cntslist = list(dist_cnts.items())
    # cntslist.sort(key=lambda x:x[0])

    # for c in cntslist:
    #     print(c[0], [c[1]])
 

    final_outputs = [raw, input_text, labels]
    #Now pickle these three to fee to linear model
    pickle_path = save_path + games_save

    with open(pickle_path, 'wb') as f:
        pickle.dump(final_outputs, f)

# if 'preds' in games:
#     #switch out output narrations with gold narrations
#     with open(open_path + gold_test, 'r') as jf:
#         goldfile = json.load(jf)
#     narr_dict = {}
#     for gg in goldfile:
#         narr_dict[gg['id']]=[rel for rel in gg['relations'] if rel['type'] == 'Narration']
#     gold_rels = []
#     for g in jfile:
#         g['relations'] = narr_dict[g['id']]
#     with open(save_path + new_games, 'w') as outfile:
#         json.dump(jfile, outfile)
#     print('test json saved')
# else:
#     with open(save_path + new_games, 'w') as outfile:
#         json.dump(jfile, outfile)
#     print('train json saved')
