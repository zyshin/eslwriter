import requests, logging

logger = logging.getLogger(__name__)

from django.conf import settings


LEMMATIZER_URL = settings.STANFORD_CORENLP_SERVER + '?properties={"outputFormat":"conll"}'


def lemmatize(s):
    '''
    s: a English string
    return: a list of lower-cased lemmas
    '''
    q=''
    if s.endswith('?'):
        s, q = s.strip('?'), '?'

    try:
        conll = requests.post(LEMMATIZER_URL, s, timeout=10).text
        tokens = [line.split('\t') for line in conll.split('\n') if line]

        #print 'token',tokens
        if len(tokens)>1:
            ll = tokens[0][2].lower()
            ref = tokens[0][1]
        else:
            ll=''
            ref=''
        #ll = [t[2].lower() if len(t)>2 else '' for t in tokens]
        #ref = [t[1] if len(t)>2 else '' for t in tokens]
        #print 'll',ll
        #print 'ref',ref
    except Exception as e:
        logger.exception('Failed to lemmatize "%s"', s)
        ll = ref = s.split()
        ll = ll.lower()

    return ll+q
