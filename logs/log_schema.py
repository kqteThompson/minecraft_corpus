import json
import os


current_folder=os.getcwd()

#if these folders don't exist in directory change paths accordingly

logfile = 'C1-B1-A3_aligned-observations.json'
log_path = current_folder + '/' + logfile

save_path= current_folder + '/log_schemas/'

if not os.path.isdir(save_path):
    os.makedirs(save_path)

game = logfile.split('_')[0]

save_name = game + '_logschema'

def make_rep(block):
    coords = block['AbsoluteCoordinates']
    tup = (coords['Y'], coords['X'], coords['Z'])
    rep = (block['Type'], tup)
    return rep


with open(log_path, 'r') as jf:
    jfile = json.load(jf)
    data = jfile['WorldStates']
    print('{} world states in game {}'.format(len(data), game))

#get final structure
final_positions = []
final = data[-1]['BlocksInGrid']
for block in final:
    rep = make_rep(block)
    final_positions.append(rep)

print('{} blocks in final structure'.format(len(final_positions)))


log_exchange = {} #keys: timestamps #val: dicts of chats and moves
previous_blocks = []
previous_chat = []
absolute_block_count = 1
for ws in data:
    exchange_element = {}
    ti = ws['Timestamp']
    chat = ws['ChatHistory']
    blocks = []
    for block in ws['BlocksInGrid']:
        rep = make_rep(block)
        blocks.append(rep)

    #diff with previous chats
    diff_chat = [x for x in chat if x not in previous_chat] #just take new utterances
    exchange_element['chat'] = diff_chat
    previous_chat = chat

    #find block moves
    move = None
    #put
    put = set(blocks).difference(set(previous_blocks))
    #if there are some in current that are not in previous, then a block was added
    if len(put) != 0:
        b = list(put)[0]
        move = {}
        move['type'] = 'Put'
        move['abs_block'] = absolute_block_count
        move['block'] = b
        if b in final_positions:
            move['final'] = 'Final'
        else:
            move['final'] = 'Nonf'

        absolute_block_count += 1

    #remove
    remove = set(previous_blocks).difference(set(blocks))
    #if there are some in previous that are not in current, then a block was removed
    if len(remove) != 0:
        b = list(remove)[0]
        move = {}
        move['type'] = 'Remove'
        move['block'] = b
        if b in final_positions:
            move['final'] = 'Final'
        else:
            move['final'] = 'Nonf'
    
    previous_blocks = blocks
    
    exchange_element['move'] = move

    log_exchange[ti] = exchange_element

    move = None


with open(save_path + save_name + '.json', 'w') as outfile:
    json.dump(log_exchange, outfile)

print('log saved')
