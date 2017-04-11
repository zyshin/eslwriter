# -*- coding: utf-8 -*-

ESL_DEP_TYPES = ['NSUBJ', 'DOBJ', 'IOBJ', 'NSUBJPASS', 'AMOD', 'NN', 'ADVMOD', 'PARTMOD', 'PREP', 'POBJ', 'PRT']
VERB_TYPES = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
PREP_TYPES = ['IN', 'TO']
ADV_TYPES = ['RB', 'RBR', 'RBS', 'RP']
ADJ_TYPES = ['JJ', 'JJR', 'JJS']
NOUN_TYPES = ['NN', 'NNP', 'NNPS', 'NNS']
# COLLOCATIONS = [u'(主谓)', u'(动宾)', u'(修饰)', u'(介词)']

def is_esl_dep(dt, t, td):
    return _is_esl_dep((dt, None, None, (None, t['l'], t['pt']), (None, td['l'], td['pt'])))

def convert_dep(dt, t, td):
    dt, t1, t2 = _convert_dep((dt, t, td, (None, t['l'], t['pt']), (None, td['l'], td['pt'])))
    return {'dt': dt, 'l1': t1['l'], 'i1': t1['i'], 'l2': t2['l'], 'i2': t2['i']}

# format of d:
# (type, None, None, token1, token2)
# format of token:
# (~word, lemma, pos)
def _is_esl_dep(d):
    if d[0] not in ESL_DEP_TYPES:
        return False
    t1 = d[3]   #TODO: filter out numbers
    t2 = d[4]   #TODO: filter out numbers
    if (t1[2] in VERB_TYPES and t1[1] == 'be') or (t2[2] in VERB_TYPES and t2[1] == 'be'):
        return False
    if d[0] == 'NSUBJ' and not (t1[2] in VERB_TYPES + ADJ_TYPES and t2[2] in NOUN_TYPES):
        return False
    if (d[0] == 'DOBJ' or d[0] == 'IOBJ' or d[0] == 'NSUBJPASS') and not (t1[2] in VERB_TYPES and t2[2] in NOUN_TYPES):
        return False
    if d[0] == 'ADVMOD' and not (t1[2] in VERB_TYPES + ADJ_TYPES + ADV_TYPES and t2[2] in ADV_TYPES):
        return False
    if d[0] == 'PARTMOD' and not (t1[2] in NOUN_TYPES and t2[2] in VERB_TYPES):
        return False
    if d[0] == 'PREP' and not (t2[2] in PREP_TYPES):
        return False
    if d[0] == 'POBJ' and not (t1[2] in PREP_TYPES):
        return False
    if d[0] == 'PRT' and not (t1[2] in VERB_TYPES and t2[2] in PREP_TYPES + ADV_TYPES):
        return False
    return True

def _convert_dep(d):
    t1 = d[3]
    t2 = d[4]
    if d[0] == 'NSUBJ' and t1[2] in VERB_TYPES:
        return (1, d[2], d[1])  #'sv'
    if d[0] == 'DOBJ' or d[0] == 'IOBJ' or d[0] == 'NSUBJPASS':
        return (2, d[1], d[2])  #'vo'
    if d[0] == 'AMOD' or d[0] == 'NN' or d[0] == 'ADVMOD':
        return (3, d[2], d[1])  #'mod'
    if d[0] == 'PARTMOD' or d[0] == 'NSUBJ':
        return (3, d[1], d[2])  #'mod'
    if d[0] == 'PREP' or d[0] == 'PRT':
        return (4, d[1], d[2])  #'prep'
    if d[0] == 'POBJ':
        return (4, d[1], d[2])  #'prep'
    #return None
