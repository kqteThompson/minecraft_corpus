"""
this will take a json game from apply_glozz and output a string
that will be saved as an aa file once it is passed back to apply_glozz
"""

import templates

def get_format(game_json):

    xml = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>', '<annotations>']

    paras = game_json['paras']
    edus = game_json['edus']

    paras.sort(key = lambda x: x['start_pos'])

    para_id = None
    for p in paras:
        para_id = p['unit_id']
        para_temp = templates.make_paragraph(para_id, p['start_pos'], p['end_pos'])
        xml.append(para_temp)

        ees = [elem for elem in edus if elem['para_id'] == para_id]
        ees.sort(key = lambda x: x['start_pos'])
        for e in ees:
            edu_temp = templates.make_edu(e['unit_id'], e['turnID'], e['minecraftSegID'], e['Speaker'], e['start_pos'], e['end_pos'])
            xml.append(edu_temp)

    for r in game_json['relations']:
        rel_temp = templates.make_relation(r['relation_id'], r['x_id'], r['y_id'], r['type'])
        xml.append(rel_temp)
    
    for c in game_json['cdus']:
        cdu_temp = templates.make_cdu(c['schema_id'], c['embedded_units'])
        xml.append(cdu_temp)

    xml.append('</annotations>')
    xml_string = '\n'.join(xml)

    return xml_string




