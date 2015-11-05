# -*- coding: utf-8 -*-
from django.conf import settings

def count():
    pipeline = [
        {'$project': {'_id': 0, 't': 1}},
        {'$unwind': '$t'},
        # {'$match': {'t.pt': {'$nin': range(1, 9) + [10, 45]}}},
        {'$group': {'_id': None, 'c': {'$sum': 1}}},
    ]
    for field in xrange(1, 10):
        s = 0
        for corpus in dbc.common.corpora.find({'field': field}):
            r = list(dbc.sentences[corpus['_id']].aggregate(pipeline))
            if r:
                s += r[0]['c']
        print s
