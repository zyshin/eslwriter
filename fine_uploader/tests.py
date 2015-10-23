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