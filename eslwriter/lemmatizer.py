import requests, logging

logger = logging.getLogger(__name__)

from django.conf import settings


LEMMATIZER_URL = settings.STANFORD_CORENLP_SERVER + '?properties={"outputFormat":"conll"}'


def lemmatize(s):
    '''
    s: one English word, may end with ?
    # return: lower & retain '?'
    '''
    q, l = '', ''
    if s.endswith('?'):
        s, q = s.strip('?'), '?'

    try:
        conll = requests.post(LEMMATIZER_URL, s, timeout=10).text  # may end with \r\n
        lines = [line.strip() for line in conll.split('\n')]
        tokens = [line.split('\t') for line in lines if line]
        logger.info('conll: "%s" -> %s', s, tokens)

        if tokens:
            l = tokens[0][2].lower()
        # ref = tokens[0][1]
    except Exception as e:
        logger.exception('Failed to lemmatize "%s"', s)
        l = s.lower()

    return l+q
