"""
Takes a json file of ANNOTATED games that have been flattened 
and squished.
Returns json ready for BERT
"""
import os 
import json 
import datetime
from collections import defaultdict 

def make_order_dict(edus):
    """
    return a dict of edu id : global index
    """
    order_dict = {}
    for edu in edus:
        order_dict[edu['unit_id']] = edu['global_index']
    return order_dict

def return_instructions(relations):
    """
    return a list of all the edus where Narr and Result meet
    as well as where the first Cont ends
    NB: these will be the first edus of an instruction sequence 
    """
    instruction_list = []
    inst_dict = defaultdict(list)
    for rel in relations:
        if rel['type'] == 'Continuation' and rel['x'] == 0:
            instruction_list.append(rel['y_id'])
        inst_dict[rel['y_id']].append(rel['type'])
    
    for item in inst_dict.items():
        if 'Narration' in item[1] and 'Result' in item[1]:
            instruction_list.append(item[0])

    return instruction_list

def _remove_corrections(snips, corrections):
    """
    takes a list of snippets and a list of y_ids that are the targets of corrections, 
    returns the list of snippets without those that contain corrections
    """
    new_snips = []
    for snip in snips:
        y_ids = [s['unit_id'] for s in snip]
        flag = 0
        for c in corrections:
            if c in y_ids:
                flag = 1
        if flag == 0:
            new_snips.append(snip)
    return new_snips


current_folder=os.getcwd()

open_path = '/home/kate/minecraft_corpus/flatten/json_flat/2023-06-12_squish.json'

save_path= current_folder + '/snippets_out/'

games = []
remove_corrections = 'yes'
#remove_multi_speaker = 'yes'

with open(open_path, 'r') as jf:
    jfile = json.load(jf)
    total_snippets = 0 #keep track of number of snippets
    total_minus_corrections = 0
    for game in jfile:
        game_dict = {}
        #get id
        game_dict['id'] = game['game_id']
        print(game['game_id'])
        #replace x,y
        order = make_order_dict(game['edus'])
        new_relations = []
        for rel in game['relations']:
            rel['x'] = order[rel['x_id']]
            rel['y'] = order[rel['y_id']]
            new_relations.append(rel)
        #re-order rels by y
        new_relations.sort(key=lambda x: x['y'])
        #create list of snippets
        snippets = []
        inst_starts = return_instructions(new_relations)

        last = 0
        for i, e in enumerate(game['edus']):
            if e['unit_id'] in inst_starts:
                snip = game['edus'][last:i]
                last = i
                snippets.append(snip)
        snippets.append(game['edus'][last:])
        
        #remove first b/c this is always matter before first instruction
        snippets = snippets[1:]
        #count snippets
        total_snippets += len(snippets)

        if remove_corrections == 'yes':
            #get a list of edus that are the targets of Correction relations
            correction_list = [r['y_id'] for r in new_relations if r['type'] == 'Correction']
            snippets = _remove_corrections(snippets, correction_list)
            total_minus_corrections += len(snippets)
     
        ind = 0
        for s in snippets:
            game_dict[ind] = s
            ind += 1


        games.append(game_dict)

    print('{} total snippets and {} without correction'.format(total_snippets, total_minus_corrections))
    
    #count the number of snippets that include more than one set of moves
    #if remove_multi_speaker == 'yes': !! REMOVE by defalt for the moment
    #return 'final games' which is all the snippets that are not multi move
    multi_moves = []
    final_games = []
    final_snips_count = 0
    for game in games:
        new_game_dict = {}
        new_game_dict['id'] = game["id"]
        index_count = 0
        snips = [item[1] for item in game.items() if item[0] != 'id']
        for snip in snips:
            speakers = [s for s in snip if s['Speaker'] == 'System']
            if len(speakers) > 1:
                multi_moves.append(game['id'] + ' ' + snip[0]['turnID'].split('.')[-1])
                # final_game_list.append(game['id'])
            else:
                new_game_dict[index_count] = snip
                index_count += 1
                final_snips_count += 1
        final_games.append(new_game_dict)
                

    print('{} snippets with multiple moves'.format(len(multi_moves)))
    
    print_string = '\n'.join(multi_moves)
    
    with open (current_folder + '/multimoves.txt', 'w') as txt_file:
        txt_file.write(print_string)

    print('{} final snippets'.format(final_snips_count))

    ##output final snippets json

    num_games = len(jfile)
    print('{} games made into snippets.'.format(num_games))    

    now = datetime.datetime.now().strftime("%Y-%m-%d")

    ##save bert json
    save_file_name = save_path + now + '_' + str(num_games) + '_snippets.json'
    
    with open(save_file_name, 'w') as outfile:
        json.dump(final_games, outfile)

    print('json saved')
    




        
        