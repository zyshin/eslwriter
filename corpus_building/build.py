import time

from django.conf import settings
from .parse import parse_files
from .collocation import is_esl_dep, convert_dep
from common.utils import *
from eslwriter.utils import *


def build_corpus(cid, parse=True, append=True):
	dbc = settings.DBC
	key = {'corpus': cid}
	if append:
		key.update({'_id': {'$nin': dbc.sentences[str(cid)].distinct('p')}})
	else:
		dbc.sentences.drop_collection(str(cid))
	uploads = list(dbc.common.uploads.find(key))
	db = dbc.common.files
	pids = tuple(set([u['file'] for u in uploads]))


	# parse
	toparse, towait = [], []
	for p in db.find({'_id': {'$in': pids}, 'status': 2}):
		pid = p['_id']
		if db.find_one_and_update({'_id': pid, 'status': 2}, {'$set': {'status': -3}}):
			toparse.append(pid)
		else:
			towait.append(pid)

	if toparse:
		print len(toparse), 'files parsing'
		r = parse_files(cid, toparse)
		dbc.common.logs.insert_one(r)
		bulk = db.initialize_unordered_bulk_op()
		for pid in toparse:
			status = 4 if parsed_path(pid, check=True) else 3
			bulk.find({'_id': pid}).update_one({'$set': {'status': status}})
		bulk.execute()
	if towait:
		print len(towait), 'files waiting'
		for i in xrange(60 * len(towait)):
			towait = [p['_id'] for p in db.find({'_id': {'$in': towait}, 'status': -3})]
			if not towait:
				break
			time.sleep(1)

	parsed_pids = [p['_id'] for p in db.find({'_id': {'$in': pids}, 'status': 4})]


	# count
	print len([1 for u in uploads if u['file'] in parsed_pids]), 'files indexing'
	# _token_dict = {}  #'word' -> count, should use {} to enable
	sentences = []
	count = 0
	db = dbc.sentences[str(cid)]
	for u in uploads:
		pid = u['file']
		if not pid in parsed_pids:
			continue
		path = parsed_path(pid)
		try:
			with open(path, 'r') as fin:
				text = fin.read()
			_sentences = process_conll_file(u['_id'], text)
			# compress
			for s in _sentences:
				if sum([t['pt'] not in pt2i for t in s['t']]):
					continue
				for t in s['t']:
					t['w'] = t2i.get(t['w'], t['w'])
					t['l'] = t2i.get(t['l'], t['l'])
					t['pt'] = pt2i.get(t['pt'], t['pt'])
				for d in s['d']:
					d['l1'] = s['t'][d['i1']]['l']
					d['l2'] = s['t'][d['i2']]['l']
				sentences.append(s)
			# sentences += _sentences
			if len(sentences) > 100000:
				print 'saving %d sentences' % len(sentences)
				db.insert_many(sentences)
				count += len(sentences)
				sentences[:] = []
		except Exception as e:
			print 'Exception when counting:', repr(e)
	if sentences:
		print 'saving %d sentences' % len(sentences)
		db.insert_many(sentences)
		count += len(sentences)
		sentences[:] = []

	# tokens = [{'_id': i+1, 't': k, 'c': v} for i,(k,v) in enumerate(sorted(token_dict.iteritems(), key=lambda kv: kv[1], reverse=True))]
	# tokens = [{'_id': t2i(t), 'c': c } for t,c in _token_dict.iteritems()]


	# index
	print 'creating index'
	db.create_index('t.l')
	db.create_index([('d.dt', 1), ('d.l1', 1), ('d.l2', 1)])
	# import math
	# for t in tokens:
	#	 t['df'] = db.sentences.find({'t.l': t['_id']}).count()
	#	 t['tfidf'] = math.log(t['c']/float(t['df']+1)) if t['c'] else 0
	# db.tokens.remove()
	# db.tokens.insert(tokens)

	return count

def process_conll_file(uid, text, token_dict=None, pos_dict=None, dep_dict=None):
	# conll file format:
	# 1  Assimilation  assimilation  NN  _  3  nsubj
	# 1  3  nsubj  =  nsubj(noun-3, verb-1)
	sentences = []
	for s in text.split('\n\n'):
		if not (s and s.strip()):
			continue
		tokens = [process_conll_line(l, token_dict, pos_dict, dep_dict) for l in s.split('\n')]
		deps = []
		for i, t in enumerate(tokens):
			assert t['i'] == i, 't[i] = %d, i = %d' % (t['_id'], i)
			td = tokens[t['di']]
			if is_esl_dep(t['dt'], td, t):
				deps.append(convert_dep(t['dt'], td, t))
			del t['dt'], t['di']
		sentences.append({'p': uid, 't': tokens, 'd': deps})
	return sentences

def process_conll_line(l, token_dict, pos_dict, dep_dict):
	tt = l.split('\t')
	assert len(tt) == 7, 'len(%s) = %d != 7' % (repr(tt), len(tt))
	if token_dict is not None:
		token_dict[tt[1]] = token_dict.get(tt[1], 0)	# count word
		token_dict[tt[2]] = token_dict.get(tt[2], 0) + 1	# count lemma
	pt = tt[3].upper()
	dt = tt[6].upper()
	if pos_dict is not None:
		pos_dict[pt] = pos_dict.get(pt, 0) + 1	# count pos type
	if dep_dict is not None:
		dep_dict[dt] = dep_dict.get(dt, 0) + 1	# count dep type
	return {'i': int(tt[0])-1, 'w': tt[1], 'l': tt[2], 'pt': pt, 'di': int(tt[5])-1, 'dt': dt}


if __name__ == "__main__":
	pass
