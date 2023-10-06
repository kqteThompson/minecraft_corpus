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

#running on training data:
# games = 'TRAIN_314_bert_2p2.json'
games = 'bert_multi_preds_30_2p2.json'
# games_save = 'TRAIN_314_bert_2p2.pck'
games_save = 'bert_multi_preds_30_2p2.pck'


#running on linear outputs:
# games = 'bert_multi_preds_30_second_pass.json'
# games_save = 'bert_multi_preds_2p1.pck'


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


MAX_LEN = 16

with open(open_path + games, 'r') as jf:
    jfile = json.load(jf)
   
    # labels = []
    # raw = []
    # input_text = []

    total_corrections = 0
    total_nl_pairs = 0
    total_first_kind = 0
    total_second_kind = 0
    same_NL = 0
    empty_NL = 0
    just_second = 0
    just_first = 0

    for game_ind, game in enumerate(jfile):

        # if game['id'] == 'C154-B29-A1':
        #make raw text 
        # raw_text = [j["speaker"][:5] + ": " + j["text"] for j in jfile[game_ind]["edus"] ]

        # raw += [raw_text]

            # print(game['id'])

            edus = game['edus']
            correls = [(e['x'], e['y']) for e in game['relations']]

            # print('{} corrections'.format(len(correls)))
            # print(correls)
            total_corrections += len(correls) #ADD

            # correction_cands = []

            #get consective NL-NL pairs
            pairs = []

            nls = [edu for edu in edus if edu['type'] == 0]
            for pair in [nls[i:i+2] for i in range(len(nls)-1)]:
                pairs.append(pair)

            total_nl_pairs += len(pairs)

            for pair in pairs:
                start = pair[0]['global_index']
                end = pair[1]['global_index']
                # print('start, end ', start, end)

                # print(start, end)
                distance = end - start

                #get number of architect turns between them
                # slice = edus[start:end]
                # num_arch = []
                # for sl in slice:
                #     if sl['speaker'] == 'Architect':
                #         num_arch.append(sl['turn'])
                # total = len(list(set(num_arch)))

                #get global indicies of architect turns in between
                slice = edus[start:end]
                num_arch = []
                for sl in slice:
                    if sl['speaker'] == 'Architect':
                        num_arch.append(sl['global_index'])
                # print('all archs: ', num_arch)
                
                #get number of corrections 
                first_corrections = [c for c in correls if c[0] == start and c[1] in num_arch]
                # print('first corrections: ', first_corrections)
                second_corrections = [c for c in correls if c[0] == start and c[1] == end]

                total_first_kind += len(first_corrections)
                total_second_kind += len(second_corrections)
                
                if len(first_corrections) > 0 and len(second_corrections) > 0 :
                    same_NL += 1
                
                if len(first_corrections) == 0 and len(second_corrections) == 0 :
                    empty_NL += 1

                if len(first_corrections) == 0 and len(second_corrections) > 0 :
                    just_second += 1
                
                if len(first_corrections) > 0 and len(second_corrections) == 0 :
                    just_first += 1
                    

                

                # #get corrections
                # corrections = [c for c in correls if c[0] >= start and c[1] <= end]

                # cor_start = [c for c in correls if c[0] == start]


            #     print('distance {}, {} arch turns in between, {} corrections, {} corr NL source'.format(distance, total, len(corrections), len(cor_start)))
            # print('\n', '-------', '\n')

                # print('distance {}, {} first corrections, {} second_corrections'.format(distance, len(first_corrections), len(second_corrections)))
                # print('\n', '-------', '\n')
            
    print('{} corrections, {} NL pairs, {} NL-Arch corrs, {} NL-NL corrs'.format(total_corrections, total_nl_pairs, total_first_kind, total_second_kind, same_NL))
    print('{} just NL-Arch, {} just NL-NL, {} both, {} empty NLs'.format(just_first, just_second, same_NL, empty_NL))
         
        



        

    #     #get candidates
    #     game_cands = []
    #     edus = game['edus']
    #     turns = get_turns(edus)
    #     #dict of turns to avoid
    #     # print(turns)

    #     ##get edu list
    #     archs = [t for t in edus if t['speaker'] != 'Builder' and t['turn_ind'] <= 3]

    #     ##make relations list for easy access during candidate production.
    #     rels = [(r['x'], r['y']) for r in game['relations']]
    #     # print(rels)

    #     for edu in archs:
    #         num = edu['turn']
    #         avoid = []
    #         #then this will be source
    #         if edu['turn'] in turns.keys():
    #             avoid = turns[edu['turn']]
    #         for target in [elem for elem in archs if elem['turn'] > num and elem['turn'] not in avoid]:
    #             cand = [game_ind, edu['global_index'], target['global_index'], 0, -1, edu['res'], edu['res']]
    #             if (cand[1], cand[2]) in rels: ##NB need to figure out how to find rels that arent captured
    #                 cand[3] = 1
    #                 cand[4] = 14
    #             game_cands.append(cand)
    #     # print(game_cands)

    #     #reduce cands to those under specified cutoff
    #     if MAX_LEN:
    #         game_cands = [c for c in game_cands if abs(c[2] - c[1]) <= MAX_LEN]
    #     # for ca in game_cands:
    #     #     print(ca[2] - ca[1])
        
    #     #create input text pairs from candidates
    
    #     text = [[raw_text[cand[1]], raw_text[cand[2]]] for cand in game_cands]
        
        
    #     labels.extend(game_cands)
    #     input_text.extend(text)

    #     print('Game {} has length {} and  has {} candidates'.format(game['id'], len(raw_text), len(game_cands)))

    # # use this to see the distance distributions
    # # distances = [abs(i[2] - i[1]) for i in labels if i[3] == 1]
    # # dist_cnts = Counter(distances)
    # # cntslist = list(dist_cnts.items())
    # # cntslist.sort(key=lambda x:x[0])

    # # for c in cntslist:
    # #     print(c[0], [c[1]])
 

    # final_outputs = [raw, input_text, labels]
    # #Now pickle these three to fee to linear model
    # pickle_path = save_path + games_save

    # with open(pickle_path, 'wb') as f:
    #     pickle.dump(final_outputs, f)


