'''
input: single dialogue text string from dialogue-with-actions.txt in minecraft corpus
**which include '&' segment splits**
output: .aa and .ac files for glozz annotation plus dialogue id
NB dialogue ids are of the form B24-A25-C48-1523056660291
'''
import os
import uuid 

def createid():
    newid = uuid.uuid1()
    return newid.fields[0]

def split_line(turn):
    idx1 = turn.find('<')
    idx2 = turn.find('>')
    if idx1 > -1:
        text = turn[idx2 + 1:]
        speaker = turn[idx1 + 1: idx2]
    else:
        text = turn
        speaker = 'sys'
    return speaker, text 

def get_format(dialogue_list):

    xml_start = ['<?xml version="1.0" ?>', '<annotations>', '<metadata/>']
    xml_end = ['</annotations>']

    ac_string = ' '

    info = dialogue_list[0].split('-')
    names = {'Architect': 'Architect_' + info[1], 
    'Builder': 'Builder_' + info[0], 
    'sys': 'System'}

    dialogue_id = info[2] + '-' + info[0] + '-' + info[1] 

    para_start_pos = 1
    turn_no = 0

    for turn in dialogue_list[1:]:

        speaker, text = split_line(turn)

        turn_speaker = names[speaker]

        texts = []

        ##check if there is a '&' split in the string

        amps = text.split('&')
        texts = [s.strip() for s in amps]

        speaker_string = str(turn_no) + ' : ' + turn_speaker + ' : '

        ac_string += speaker_string

        for text in texts:

            ac_string += text + ' '

        ##create units for each segment in the turn
        seg_xml = []

        seg_start_pos = para_start_pos + len(speaker_string)
        
        for segment in texts:

            #seg_start_pos = para_start_pos + len(speaker_string)

            seg_end_pos = seg_start_pos + len(segment)

            #create turn id new segment for each text segment in texts
            turn_id = dialogue_id + '.' + turn_speaker + '.' + str(turn_no)

            act_id = createid()
          
            act_xml = ['<unit id="' + str(act_id) + '_minecraft">','<metadata>','<author>minecraft</author>',
            '<creation-date>0</creation-date>','<lastModifier>minecraft</lastModifier>',
            '<lastModificationDate>0</lastModificationDate>','</metadata>','<characterisation>',
            '<type>Segment</type>','<featureSet>','<feature name="turnID">' + turn_id + '</feature>',
            '<feature name="minecraftSegID">' + str(act_id) + '_' + turn_speaker + '</feature>',
            '<feature name="Speaker">' + turn_speaker + '</feature>','</featureSet>','</characterisation>',
            '<positioning>','<start>','<singlePosition index="'+ str(seg_start_pos) +'"/>','</start>','<end>',
            '<singlePosition index="'+ str(seg_end_pos) +'"/>','</end>','</positioning>','</unit>']

            seg_xml.extend(act_xml)

            seg_start_pos = seg_end_pos + 1

        para_end_pos = seg_end_pos + 1

        #create a new paragraph
        para_xml = ['<unit id="minecraft_'+ str(turn_no) +'">','<metadata>','<author>minecraft</author>','<creation-date>0</creation-date>',
        '</metadata>','<characterisation>','<type>paragraph</type>','<featureSet/>','</characterisation>','<positioning>',
        '<start>','<singlePosition index="'+ str(para_start_pos) +'"/>','</start>','<end>','<singlePosition index="'+ str(para_end_pos) 
        +'"/>','</end>','</positioning>','</unit>']

        xml_start.extend(para_xml)

        xml_start.extend(seg_xml)

        #update counters
        turn_no +=1
        para_start_pos = para_end_pos

    xml_start.extend(xml_end)

    aa_string = '\n'.join(xml_start)

    return ac_string, aa_string, dialogue_id

