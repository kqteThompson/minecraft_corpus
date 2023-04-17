import json
import os
from datetime import datetime


current_folder=os.getcwd()

json_path= current_folder + '/log_schemas/'

game = 'C1-B1-A3_logschema.json'

save_name = current_folder + '/'

with open(json_path + game, 'r') as jf:
    data = json.load(jf)
    
text_list = []
text_list.append(['time', 'arch', 'builder', 'move', 'block', 'final'])
for key in data.keys():
    key = datetime.strptime(key, '%Y-%m-%d %H:%M:%S')
for k,v  in sorted(data.items()):
    row = []
    row.append(k.split(' ')[1])
    u = v['chat']
    if len(u) > 0:
        if 'Builder' in u:
            row.extend([None, u])
        else:
            row.extend([u, None])
    else:
        row.extend([None, None])
    m = v['move']
    if m:
        t = m['type']
        b = m['block'][0]
        row.extend([t,b])
        f = m['final']
        if f == 'Final':
            row.append('final')
        else:
            row.append('non-final')
    else:
        row.extend([None, None, None])
    text_list.append(row)

for t in text_list:
    print(t)
    print('------')
# with open(save_path + save_name + '.json', 'w') as outfile:
#     json.dump(log_exchange, outfile)

# print('log saved')
