from prashant import BuilderAction, BuilderActionExample

def get_next_builder_actions(builder_moves):
    """
    takes a list of builder moves 
    e.g. 1bl1o 1bl2o 0bl2o 0bl1o 1bl1i 1bl2i 1bl3i 
    returns a list of BuilderActionExample objects
    {
    action_type: str, 
    block: {x:int, y:int, z:int type: str}
    }
    """
   
    xdict = {'b':-5, 'c':-4, 'd':-3, 'f':-2, 'g':-1, 'h':0, 
             'j':1, 'k':2, 'l':3, 'm':4, 'n':5}
    zdict = {'a':-5, 'e':-4, 'i':-3, 'o':-2, 'u':-1, 'p':0, 
             'q':1, 'r':2, 'x':3, 'y':4, 'z':5}

    colors = {'r':'red', 'b':'blue', 'g':'green', 
               'o':'orange', 'y':'yellow', 'p':'purple'}
    actions = {'0': 'pickup', '1': 'putdown'}
    moves = builder_moves.split(' ')
    builder_actions = []
    for move in moves:
        move = move.strip()
        if move == 'SKIP':
            continue
        else:
            elem_action = actions[move[0]]
            elem_type = colors[move[1]]
            elem_x = int(xdict[move[2]])
            elem_y = int(move[3])
            elem_z = int(zdict[move[4]])
            weight = None
            
            action = BuilderAction(elem_x, elem_y, elem_z, elem_type, elem_action, weight)
            builder_actions.append(action)

    return builder_actions

def get_instruction(ling_moves):
    """
    takes a list of tuples from the snippet
    returns linguistic moves in a list of dicts
    [{'speaker':str, 'utterance':tokens in strings},{...}]
    """
    utt_list = []
    speaker_dict = {}
    last_speaker = None
    for move in ling_moves:
        if move[0] != last_speaker:
            if bool(speaker_dict) == False:
                speaker_dict['speaker'] = move[0]
                speaker_dict['utterance'] = move[1]
            else:
                utt_list.append(speaker_dict)
                last_speaker = move[0]
                speaker_dict = {}
                speaker_dict['speaker'] = move[0]
                speaker_dict['utterance'] = move[1]
        else:
            speaker_dict['utterance'].extend(move[1])
    if bool(speaker_dict) == True:
        utt_list.append(speaker_dict)
    return utt_list

def isSubsequence(x, y):
    it = iter(y)
    return all(any(c == ch for c in it) for ch in x)

def format_prev_config(pg):
    """
    takes a list of dicts and returns it without Abs/Persp 
    coordinate distinction
    """
    config = []
    for d in pg:
        new_d = {}
        new_d['type'] = d['Type'].split('_')[2]
        new_d['x'] = d['AbsoluteCoordinates']['X']
        new_d['y'] = d['AbsoluteCoordinates']['Y']
        new_d['z'] = d['AbsoluteCoordinates']['Z']
        config.append(new_d)
    return config

def format_build_pos(pd):
    """
    takes a prev builder position dict and returns same
    but with lower case keys
    """
    pos = {}
    pos['x'] = pd['X']
    pos['y'] = pd['Y']
    pos['z'] = pd['Z']
    pos['yaw'] = pd['Yaw']
    pos['pitch'] = pd['Pitch']
    return pos 

def return_state_info(worldstates, speaker, utterance, start_index):
    """
    Takes a list of observed world states from logs, last speaker, 
    last utterance, and the index after which the last snippet was found
    so not to run through all worldstates again
    Returns:
    prev_config [list of dicts]
    prev_builder_position [dict]
    sample_id (index) [int] (used for the next snippet)
    """
    prev_builder_position = {}
    sample_id = None
    prev_config = None
    for log in worldstates[start_index:]:
        if 'first_chat' in log.keys():
            #check if speakers match
            for turn in log['first_chat']['tokens']:
                if turn[0] == speaker:
                    #see if tokens match
                    # print('---matching---')
                    # print(log['state_index'])
                    # print(turn[1])
                    # print(utterance)
                    if isSubsequence(utterance, turn[1]):
                        # print('matched {}!!'.format(log['state_index']))
                        sample_id = log['state_index']
                        prev_builder_position = format_build_pos(log['BuilderPosition'])
                        prev_config = format_prev_config(log['BlocksInGrid'])
                        #break
                        return sample_id, prev_builder_position, prev_config
    return start_index - 1, None, None

def get_built_config(prev_config, actions):
    """
    takes a previous config and a set of builder actions and returns the 
    amended config
    NB: only use absolute coordinates...
    """
    built_config = []
  
    abs_prev = []
    new_remove = []
    new_put = []
    if prev_config:
        for move in prev_config:
            # color = move['Type'].split('_')[2]
            # abs_prev.append((color, move['X'], move['Y'], move['Z']))
            color = move['type']
            abs_prev.append((color, move['x'], move['y'], move['z']))
    for move in actions: ##needed to make this compatible with the BuilderAction Class instances
        #if move['action_type'] == 'placement':
        if move.get_action() == 'placement':
            #new_put.append((move['block']['type'], move['block']['x'], move['block']['y'], move['block']['z']))
            new_put.append(move.get_coords())
        else:
            new_remove.append(move.get_coords())
            # new_remove.append((move['block']['type'], move['block']['x'], move['block']['y'], move['block']['z']))

    #check to see if there are any cancelations
    abs_prev.extend(new_put)
    final_config = [m for m in abs_prev if m not in new_remove]
    
    #reformat
    for block in final_config:
        b = {}
        b = {}
        b['y'] = block[2]
        b['x'] = block[1]
        b['z'] = block[3]
        # b['type'] = 'cwc_minecraft_' + block[0] + '_rn'
        b['type'] = block[0]
        built_config.append(b)

    #last check
    if len(built_config) != len(final_config):
        print('ERROR IN FINAL CONFIG')

    return built_config


  