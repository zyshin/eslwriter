# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from bson.son import SON

# @user_passes_test(lambda user: user.is_superuser)
def venue_view(request):
    user = request.user
    db = settings.DBC.esl
    db_sentences = settings.DBC.sentences
    db_dblp = settings.DBC.dblp
    db_doaj = settings.DBC.doaj
    update_time = 0
    #updates = db_dblp.log.find({'type': 'update'}).sort('time': -1)
    #update_time = updates[0]['time']
    #update_new = updates[0]['info']['nNew']
    #update_old = updates[0]['info']['nOld']
    #update_inserted = updates[0]['info']['nInserted']
    #update_updated = updates[0]['info']['nUpdated']
    articles_journal = []
    articles_subject = []
    arxiv_subject = []
    pipeline1 = [
        {"$group": {"_id": "$subject", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]
    pipeline2 = [
        {"$group": {"_id": "$bibjson.journal.title", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
    ]
    # articles_journal_count = 0
    # articles_journal_display = []
    articles_subject = list(db_doaj.articles.aggregate(pipeline1))
    arxiv_subject = list(db_doaj.arxiv.aggregate(pipeline1))
    articles_journal = list(db_doaj.articles.aggregate(pipeline2))
    articles_journal_count = len(articles_journal)
    articles_journal_display = articles_journal[0:19]

    ccfa = []
    aN = an = ap = 0
    for v in db.venues.find({'ccf': 'A'}):
        N = db.papers.find({'venue': v['_id'], 'info.type': {'$ne': 'proceedings'}}).count()
        n = db.papers.find({'venue': v['_id'], 'downloaded': True}).count()
        aN += N
        an += n
        S = v.get('shortName', v['fullName'])
        s = v['dblp']
        name = '%s (%s)' % (S, s) if user.is_superuser else S
        senNum = db_sentences[s].count()
        field = v['field']
        impFac = v['impactFactor']
        ccfa.append({'name': name, 'n': n, 'N': N, 'p': float(n * 100) / N, 'senNum': senNum, 'field': field, 'impactFactor': impFac})
    ccfb = []
    bN = bn = bp = 0
    for v in db.venues.find({'ccf': 'B', 'c': {'$exists': True}}):
        N = db.papers.find({'venue': v['_id'], 'info.type': {'$ne': 'proceedings'}}).count()
        n = db.papers.find({'venue': v['_id'], 'downloaded': True}).count()
        bN += N
        bn += n
        S = v.get('shortName', v['fullName'])
        s = v['dblp']
        name = '%s (%s)' % (S, s) if user.is_superuser else S
        senNum = db_sentences[s].count()
        field = v['field']
        impFac = v['impactFactor']
        ccfb.append({'name': name, 'n': n, 'N': N, 'p': float(n * 100) / N, 'senNum': senNum, 'field': field, 'impactFactor': impFac})

    ccfa.sort(key = lambda v: v['name'])
    ccfb.sort(key = lambda v: v['name'])
    ap = float(an * 100) / aN
    bp = float(bn * 100) / bN
    #return render(request, 'monitor/venue.html', {'update_time': update_time, 'update_new': update_new, 'update_old': update_old, 'update_inserted': update_inserted, 'update_updated': update_updated, 'articles_journal': articles_journal, 'articles_subject': articles_subject, 'arxiv_subject': arxiv_subject, 'articles_journal_count': articles_journal_count, 'articles_journal_display': articles_journal_display, 'ccfa': ccfa, 'ccfb': ccfb, 'aN': aN, 'an': an, 'bN': bN, 'bn': bn, 'ap': ap, 'bp': bp})
    return render(request, 'monitor/venue.html', {'update_time': update_time, 'articles_journal': articles_journal, 'articles_subject': articles_subject, 'arxiv_subject': arxiv_subject, 'articles_journal_count': articles_journal_count, 'articles_journal_display': articles_journal_display, 'ccfa': ccfa, 'ccfb': ccfb, 'aN': aN, 'an': an, 'bN': bN, 'bn': bn, 'ap': ap, 'bp': bp})
