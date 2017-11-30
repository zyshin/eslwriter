import json
import logging
import os
import re
import string
import shutil
import hashlib
import commands
from xml.etree import ElementTree

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
#from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse

from fine_uploader.utils import make_response
from fine_uploader.models import Corpus, Paper

from eslwriter.views import init

def test_view(request, cid):
    corpus = get_object_or_404(Corpus, pk=cid)
    
    '''for p in papers:
        path = os.path.join(settings.UPLOAD_DIRECTORY, p.qquuid, 'content.txt')
        root = ElementTree.parse(path)
        paras = root.find('Paragraphes')
        outpath = os.path.join(settings.UPLOAD_DIRECTORY, p.qquuid, 'refined.txt')
        outfile = file(outpath, 'w')
        for para in paras:
            sents = para.find('Sentences')
            for sent in sents:
                s = filter(lambda c: c in string.printable, sent.find('Text').text)
                outfile.write(s + '\n')
            outfile.write('\n\n')
        outfile.close()
        p.title = root.find('Title').text
        p.save()
        print p.pk, p.title
        #break
    #return redirect(reverse('corpus', args=[cid]))'''
    return make_response(content=json.dumps('success'))

def update_word_count(corpus):
    corpus = get_object_or_404(Corpus, pk=cid)
    
    '''for p in papers:
        path = os.path.join(settings.UPLOAD_DIRECTORY, p.qquuid, 'content.txt')
        root = ElementTree.parse(path)
        paras = root.find('Paragraphes')
        outpath = os.path.join(settings.UPLOAD_DIRECTORY, p.qquuid, 'refined.txt')
        outfile = file(outpath, 'w')
        for para in paras:
            sents = para.find('Sentences')
            for sent in sents:
                s = filter(lambda c: c in string.printable, sent.find('Text').text)
                outfile.write(s + '\n')
            outfile.write('\n\n')
        outfile.close()
        p.title = root.find('Title').text
        p.save()
        print p.pk, p.title
        #break
    #return redirect(reverse('corpus', args=[cid]))'''
    return make_response(content=json.dumps('success'))

def remove_unused_papers(corpus):
    papers = Paper.objects.filter(corpus=corpus)
    for p in papers:
        pass

def test_read():
    global all_words, word_dict, all_poss, pos_dict, all_deps, dep_dict, lemma_index, all_dfs, dep_index, sentences, papers
    import cPickle
    lemma_index = cPickle.load(open(os.path.join(settings.DATA_DIR, 'lemma_index.bin'), 'rb'))
    all_dfs = cPickle.load(open(os.path.join(settings.DATA_DIR, 'all_dfs.bin'), 'rb'))
    dep_index = cPickle.load(open(os.path.join(settings.DATA_DIR, 'dep_index.bin'), 'rb'))
    sentences = cPickle.load(open(os.path.join(settings.DATA_DIR, 'sentences.bin'), 'rb'))

def test_init():
    global all_words, word_dict, all_poss, pos_dict, all_deps, dep_dict, lemma_index, all_dfs, dep_index, sentences, papers
    lines = file(os.path.join(settings.DATA_DIR, 'words'), 'r').readlines()
    all_words = tuple([''] + [l.strip() for l in lines])
    N = len(all_words)
    word_dict = dict(zip(all_words, xrange(N)))
    
    lines = file(os.path.join(settings.DATA_DIR, 'poss'), 'r').readlines()
    all_poss = tuple([''] + [l.strip() for l in lines])
    pos_dict = dict(zip(all_poss, xrange(len(all_poss))))
    
    lines = file(os.path.join(settings.DATA_DIR, 'deps'), 'r').readlines()
    all_deps = tuple([''] + [l.strip().decode('utf-8') for l in lines])
    dep_dict = dict(zip(all_deps, xrange(len(all_deps))))

    print 'loading lemma_index'
    lemma_index = [()] * N
    all_dfs = [0] * N
    with open(os.path.join(settings.DATA_DIR, 'lemma_index'), 'r') as f:
        lemma_id = 1
        for line in f:
            ss = [int(s) for s in line.split()]
            if ss:
                all_dfs[lemma_id] = ss[0]
                #lemma_index[lemma_id] = tuple([(ss[i], ss[i+1]) for i in xrange(1, len(ss), 2)])
                lemma_index[lemma_id] = tuple(ss[1:])
            lemma_id += 1
    all_dfs = tuple(all_dfs)
    lemma_index = tuple(lemma_index)
    
    print 'loading dep_index'
    with open(os.path.join(settings.DATA_DIR, 'dep_index'), 'r') as f:
        n = int(f.readline())
        dep_index = [None] * n
        dep_id = 0
        for line in f:
            ss = [int(s) for s in line.split()]
            key = tuple(ss[0:3])
            ss = ss[3:]
            #value = tuple([(ss[i], ss[i+1], ss[i+2]) for i in xrange(0, len(ss), 3)])
            value = tuple(ss)
            dep_index[dep_id] = (key, value)
            dep_id += 1
    dep_index = dict(dep_index)
    
    print 'loading sentences'
    with open(os.path.join(settings.DATA_DIR, 'sentences'), 'r') as f:
        n = int(f.readline())
        sentences = [None] * n
        for sid in xrange(n):
            pid = int(f.readline())
            m = int(f.readline())
            tokens = [None] * (3*m)
            for tid in xrange(m):
                ss = [int(s) for s in f.readline().split()]
                #tokens[tid] = tuple(ss)
                tokens[3*tid] = ss[0]
                tokens[3*tid+1] = ss[1]
                tokens[3*tid+2] = ss[2]
            tokens = tuple(tokens)
            sentences[sid] = (pid, tokens)
    sentences = tuple(sentences)

    #papers = Paper.objects.all()
    #papers = dict([(p.pk, p) for p in papers])

    print 'writing binaries'
    #import cPickle
    #cPickle.dump(lemma_index, open('lemma_index.bin', 'wb'))
    #cPickle.dump(all_dfs, open('all_dfs.bin', 'wb'))
    #cPickle.dump(dep_index, open('dep_index.bin', 'wb'))
    #cPickle.dump(sentences, open('sentences.bin', 'wb'))
'''
def processPaperList(corpus, dirname):
    title = []
    author = []
    f = open(dirname + 'paper list.txt', 'r')
    count = 0
    line = f.readline()
    while len(line) > 0:
        parts = line.split(':: ')
        title.append(parts[0])
        authorParts = parts[1].split(' ;')
        s = ''
        for i in range(len(authorParts)):
            name = authorParts[i].split(',')[0]
            s = s + name;
            if i < len(authorParts) - 1:
                s = s + '; '
        author.append(s)
        count += 1
        line = f.readline()
    f.close()
    files = [s[:-4] for s in os.listdir(dirname) if s[-4:] == '.pdf']
    if len(files) != count:
        print 'Count Error!'
        return False
    for i in xrange(count):
        papers = Paper.objects.filter(corpus=corpus, author=files[i], source='UIST\'10')
        if papers.count() > 1:
            print 'Multiple paper'
            return False
        if papers.count() == 1:
            p = papers.first()
            p.title = title[i]
            p.author = author[i]
            p.save()
            print p.pk, 'affected!'
    return True
'''
