
def get_next_builder_actions(builder_moves):
    """
    takes a list of builder moves 
    e.g. 1bl1o 1bl2o 0bl2o 0bl1o 1bl1i 1bl2i 1bl3i 
    returns a list of BuilderAction objects
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
    actions = {'0': 'removal', '1': 'placement'}
    moves = builder_moves.split(' ')
    builder_actions = []
    for move in moves:
        move = move.strip()
        if move == 'SKIP':
            continue
        else:
            new_obj = {}
            block_obj = {}
            new_obj['action_type'] = actions[move[0]]
            block_obj['type'] = colors[move[1]]
            block_obj['x'] = int(xdict[move[2]])
            block_obj['y'] = int(move[3])
            block_obj['z'] = int(zdict[move[4]])
            new_obj['block'] = block_obj
            builder_actions.append(new_obj)

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
    for log in worldstates[start_index:]:
        if 'first_chat' in log.keys():
            #check if speakers match
            for turn in log['first_chat']['tokens']:
                if turn[0] == speaker:
                    #see if tokens match
                    if isSubsequence(utterance, turn[1]):
                        sample_id = log['state_index']
                        prev_builder_position = log['BuilderPosition']
                        prev_config = log['BlocksInGrid']
                        break
    return sample_id, prev_builder_position, prev_config

def get_built_config(prev_config, actions):
    """
    takes a previous config and a set of builder actions and returns the 
    amended config
    NB: only use absolute coordinates...otherwise I will have to get these another way
    EX: 'in a line?'
    [{'action_type': 'placement', 'block': {'type': 'blue', 'x': 3, 'y': 3, 'z': -1}}, 
    {'action_type': 'placement', 'block': {'type': 'blue', 'x': 3, 'y': 3, 'z': -2}}]
    [{'PerspectiveCoordinates': 
    {'Y': -0.6689363460755829, 'X': -0.14414329148100002, 'Z': 2.351966597640045}, 
    'AbsoluteCoordinates': {'Y': 1, 'X': 3, 'Z': 0}, 'Type': 'cwc_minecraft_blue_rn'}, 
    {'PerspectiveCoordinates': 
    {'Y': -0.18090170094577887, 'X': 0.48720931447899996, 'Z': 2.9546406987097904}, 
    'AbsoluteCoordinates': {'Y': 1, 'X': 4, 'Z': 0}, 'Type': 'cwc_minecraft_red_rn'}, 
    {'PerspectiveCoordinates': 
    {'Y': 0.10821038424041712, 'X': -0.14414329148100002, 'Z': 1.7226471560540453}, 
    'AbsoluteCoordinates': {'Y': 2, 'X': 3, 'Z': 0}, 'Type': 'cwc_minecraft_blue_rn'}, 
    {'PerspectiveCoordinates': 
    {'Y': 0.5962450293702212, 'X': 0.48720931447899996, 'Z': 2.3253212571237905}, 
    'AbsoluteCoordinates': {'Y': 2, 'X': 4, 'Z': 0}, 'Type': 'cwc_minecraft_red_rn'}, 
    {'PerspectiveCoordinates': 
    {'Y': 0.8853571145564171, 'X': -0.14414329148100002, 'Z': 1.0933277144680453}, 
    'AbsoluteCoordinates': {'Y': 3, 'X': 3, 'Z': 0}, 'Type': 'cwc_minecraft_blue_rn'}]

    """
    built_config = {}
    # abs_prev = []
    # for block in prev_config:
    #     color = block['Type']
    #     coords = block['AbsoluteCoordinates']
    return built_config