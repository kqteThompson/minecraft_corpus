import os
# from collections import defaultdict

"""
using textfile of squished games, for each pair of consecutive moves, return:
game_id:
M1 - 1/0, %moves in M1 changed, correction? - M2
"""

def undone(source, target):
    """
    For the moves in source, how many of them are undone by a move in target
    """
    source = source.split(' ')
    target = target.split(' ')
    # print('source : ', source)
    # print('target : ', target)
    source_ones = []
    source_zeros = []
    target_ones = []
    target_zeros = []
    for s in source:
        if s[0] == '1':
            source_ones.append(s[1:])
        else:
            source_zeros.append(s[1:])
    for t in target:
        if t[0] == '1':
            target_ones.append(t[1:])
        else:
            target_zeros.append(t[1:])
    total = len(source) #try with target text as a denominator
    count = 0
    for e in source_ones: 
        if e in target_zeros:
            count += 1
    for e in source_zeros:
        if e in target_ones:
            count += 1
    # print(count)
    # print(total)
    # print(round(count/total, 2))
    return round(count/total, 2)
    
current_folder=os.getcwd()

corpus_path = current_folder + '/corrections_squish.txt'


moves_list = []
with open(corpus_path) as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip(' \n')
        if len(line) == 0 :
            continue
        else:
            if line[0] == 'B':
                moves_list.append('\n\n')
                moves_list.append(line)
                print(line)
                last_moves = None
            else:
                if '<system>' in line:
                    num = line.split('<')[0].strip()
                    moves = line.split('||')[1]
                    if len(moves) == 0:
                        continue
                    else:
                        if last_moves:
                            comp = undone(last_moves, moves)
                            last_moves = moves
                        else: 
                            last_moves = moves
                            comp = '0'
                        # print(num, moves)
                        if 'Correction' in line:
                            corr = line.split('|')[1].split(',')[0]
                            # print(corr)
                        else : corr = "NA"
                        moves_list.append(num + ' ' + corr + ' ' + str(comp) + ' ' + moves)


# for m in moves_list:
#     print(m)

print_string = '\n'.join(moves_list)
with open (current_folder+ '/block_changes.txt', 'w') as txt_file:
    txt_file.write(print_string)          
        
