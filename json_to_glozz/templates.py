

def make_paragraph(pid, start, end):

    tmp = ['<unit id="'+ pid +'">','<metadata>','<author>minecraft</author>','<creation-date>0</creation-date>',
    '<lastModifier>n/a</lastModifier>','<lastModificationDate>0</lastModificationDate>',
    '</metadata>','<characterisation>','<type>paragraph</type>','<featureSet/>','</characterisation>',
    '<positioning>','<start>','<singlePosition index="'+str(start)+'"/>','</start>','<end>',
    '<singlePosition index="'+str(end)+'"/>','</end>','</positioning>','</unit>']

    tmp_string = '\n'.join(tmp)
    return tmp_string

def make_edu(eid, turn, seg, speaker, start, end):
    tmp = ['<unit id="'+ eid +'">','<metadata>','<author>minecraft</author>','<creation-date>0</creation-date>',
    '<lastModifier>n/a</lastModifier>','<lastModificationDate>0</lastModificationDate>',
    '</metadata>','<characterisation>','<type>Segment</type>','<featureSet>',
    '<feature name="turnID">'+ turn +'</feature>','<feature name="minecraftSegID">'+ seg +'</feature>',
    '<feature name="Speaker">'+ speaker +'</feature>','</featureSet>','</characterisation>',
    '<positioning>','<start>','<singlePosition index="'+str(start)+'"/>','</start>','<end>',
    '<singlePosition index="'+str(end)+'"/>','</end>','</positioning>','</unit>']
   
    tmp_string = '\n'.join(tmp)
    return tmp_string

def make_relation(rid, x, y, type):
    tmp = ['<relation id="'+ rid +'">','<metadata>','<author>anonymous</author>','<creation-date>0</creation-date>',
    '<lastModifier>n/a</lastModifier>','<lastModificationDate>0</lastModificationDate>',
    '</metadata>','<characterisation>','<type>'+ type +'</type>','<featureSet/>','</characterisation>','<positioning>',
    '<term id="'+ x +'"/>','<term id="'+ y +'"/>','</positioning>','</relation>']

    tmp_string = '\n'.join(tmp)
    return tmp_string

def make_cdu(cid, embed_units):
    tmp = ['<schema id="'+ cid +'">','<metadata>','<author>nasher</author>',
    '<creation-date>0</creation-date>',
    '<lastModifier>n/a</lastModifier>','<lastModificationDate>0</lastModificationDate>',
    '</metadata>','<characterisation>', '<type>Complex_discourse_unit</type>','<featureSet/>',
    '</characterisation>','<positioning>']
    for embed in embed_units:
        if 'minecraft' in embed:
            tmp.append('<embedded-unit id="'+ embed +'"/>')
        else: 
            tmp.append('<embedded-schema id="'+ embed +'"/>')
    tmp.extend(['</positioning>','</schema>'])

    tmp_string = '\n'.join(tmp)
    return tmp_string

    

