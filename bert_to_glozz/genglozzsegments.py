'''
input: single game in json format with predicted relations
output: .aa and .ac files for glozz plus dialogue id

need the header to look like this:

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<annotations>
<metadata corpusHashcode="3797-98460153"/>
<unit id="minecraft_-1">

'''
import os
import json
import uuid 

def create_rel_xml(source, target, type):
    if type == 'QAP':
        type = 'Question-answer_pair'
    relid = createid()
    xml = ['<relation id="minecraft_' + str(relid) + '">', '<metadata>', '<author>kthompson</author>',
    '<creation-date>0</creation-date>','<lastModifier>n/a</lastModifier>',
    '<lastModificationDate>0</lastModificationDate>','</metadata>', '<characterisation>']
    reltype = '<type>' + type + '</type>'
    xml.append(reltype)
    xml.extend(['<featureSet/>','</characterisation>','<positioning>'])
    src = '<term id="' + source + '"/>'
    tgt = '<term id="' + target + '"/>'
    xml_end = ['</positioning>', '</relation>']
    xml.append(src)
    xml.append(tgt)
    xml.extend(xml_end)
    return xml

def create_seg_xml(seg_no, act_id, turn_id, turn_speaker, seg_start_pos, seg_end_pos):
    act_xml = ['<unit id="minecraft_-'+ str(seg_no) +'">','<metadata>','<author>minecraft</author>',
                '<creation-date>0</creation-date>','<lastModifier>minecraft</lastModifier>',
                '<lastModificationDate>0</lastModificationDate>','</metadata>','<characterisation>',
                '<type>Segment</type>','<featureSet>','<feature name="turnID">' + turn_id + '</feature>',
                '<feature name="minecraftSegID">' + str(act_id) + '_' + turn_speaker + '</feature>',
                '<feature name="Speaker">' + turn_speaker + '</feature>','</featureSet>','</characterisation>',
                '<positioning>','<start>','<singlePosition index="'+ str(seg_start_pos) +'"/>','</start>','<end>',
                '<singlePosition index="'+ str(seg_end_pos) +'"/>','</end>','</positioning>','</unit>']
    return act_xml

def create_para_xml(turn_no, para_start_pos, para_end_pos):
    xml = ['<unit id="minecraft_-'+ str(turn_no) +'">','<metadata>','<author>minecraft</author>','<creation-date>0</creation-date>',
            '</metadata>','<characterisation>','<type>paragraph</type>','<featureSet/>','</characterisation>','<positioning>',
            '<start>','<singlePosition index="'+ str(para_start_pos) +'"/>','</start>','<end>','<singlePosition index="'+ str(para_end_pos) 
            +'"/>','</end>','</positioning>','</unit>']
    return xml 

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

def get_format(game):

    # xml_start = ['<?xml version="1.0" ?>', '<annotations>', '<metadata/>']
    xml_start = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>', 
    '<annotations>', '<metadata corpusHashcode="3797-98460153"/>']
    xml_end = ['</annotations>']

    ac_string = ' '

    dialogue_id = game['id']

    para_start_pos = 1
    turn_no = 0
    last_speaker = game['edus'][0]['speaker']
    print('last speaker', last_speaker)
    texts = [] #put together all the edus in a turn

    edu_id_dict = {} #keep track of new edu ids via indexes
    edu_counter = 0

    paragraph_no = 1 ##add paragraph number
    seg_unit_no = 2

    for edu in game['edus']:

        turn_speaker = edu['speaker']

        if turn_speaker == last_speaker:
            texts.append(edu['text'])
        else:
            speaker_string = str(turn_no) + ' : ' + last_speaker + ' : '

            ac_string += speaker_string

            for text in texts:

                ac_string += text + ' '

            ##create units for each segment in the turn
            seg_xml = []

            seg_start_pos = para_start_pos + len(speaker_string)
            
            for segment in texts:

                seg_end_pos = seg_start_pos + len(segment)

                #create turn id new segment for each text segment in texts
                turn_id = dialogue_id + '.' + last_speaker + '.' + str(turn_no)

                act_id = createid()

                # edu_id_dict[str(edu_counter)] = str(act_id) + '_minecraft'
                edu_id_dict[str(edu_counter)] = 'minecraft_-' + str(seg_unit_no)
                edu_counter += 1
                
                act_xml = create_seg_xml(seg_unit_no, act_id, turn_id, last_speaker, seg_start_pos, seg_end_pos)

                seg_xml.extend(act_xml)

                seg_unit_no += 1

                seg_start_pos = seg_end_pos + 1

            para_end_pos = seg_end_pos + 1

            #create a new paragraph
            para_xml = create_para_xml(paragraph_no, para_start_pos, para_end_pos)

            xml_start.extend(para_xml)

            xml_start.extend(seg_xml)

            #update counters
            turn_no +=1
            para_start_pos = para_end_pos
            texts = []
            last_speaker = turn_speaker
            texts.append(edu['text'])
            paragraph_no = seg_unit_no 
            seg_unit_no = paragraph_no + 1
    
    #add last edu
    if len(texts) > 0:
        speaker_string = str(turn_no) + ' : ' + turn_speaker + ' : '

        ac_string += speaker_string

        for text in texts:

            ac_string += text + ' '

        ##create units for each segment in the turn
        seg_xml = []

        seg_start_pos = para_start_pos + len(speaker_string)
        
        for segment in texts:

            seg_end_pos = seg_start_pos + len(segment)

            #create turn id new segment for each text segment in texts
            turn_id = dialogue_id + '.' + turn_speaker + '.' + str(turn_no)

            act_id = createid()

            edu_id_dict[str(edu_counter)] = 'minecraft_-' + str(seg_unit_no)
            edu_counter += 1
        
            act_xml = create_seg_xml(seg_unit_no, act_id, turn_id, turn_speaker, seg_start_pos, seg_end_pos)

            seg_xml.extend(act_xml)

            seg_unit_no += 1

            seg_start_pos = seg_end_pos + 1

        para_end_pos = seg_end_pos + 1

        #create a new paragraph
        para_xml = create_para_xml(paragraph_no, para_start_pos, para_end_pos)

        xml_start.extend(para_xml)

        xml_start.extend(seg_xml)

    #now add relations to xml
    for rel in game['relations']:
        source = edu_id_dict[str(rel['x'])]
        target = edu_id_dict[str(rel['y'])]
        reltype = rel['type']
        rel_xml = create_rel_xml(source, target, reltype)
        xml_start.extend(rel_xml)

    xml_start.extend(xml_end)

    aa_string = '\n'.join(xml_start)

    return ac_string, aa_string, dialogue_id

