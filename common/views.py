from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import *
from .forms import *
from .utils import *


@login_required
# @user_passes_test(lambda user: settings.DBC.common.users.find_one({'_id': user.pk}), login_url='/accounts/field/')
def profile_view(request):
	# if request.user.is_superuser:
	# 	clist = Corpus.objects.all().order_by('-user__is_superuser', 'user__pk', 'date_created')
	# 	# glist = []
	# else:
	# 	# glist = Corpus.objects.filter(ispublic=True).exclude(user=request.user).order_by('-ispublic', 'date_created')
	# 	clist = Corpus.objects.filter(user=request.user).order_by('date_created')   #TODO: considering status
	key = {'_id': request.user.pk}
	profile = settings.DBC.common.users.find_one_and_update(key, {'$setOnInsert': key}, upsert=True)
	if request.user.is_superuser:
		clist = list(mongo_get_objects(Corpus, user=request.user.pk))
		clist.sort(key=lambda c: c['name'])
		for c in clist:
			c['pk'] = c['db']
			c['paper_count'] = mongo_get_objects(UploadRecord, corpus=c['db']).count()
	else:
		clist = UserCorpus.objects.filter(user=request.user)
		selected_cid = profile and profile.get('pri_corpus')
		for c in clist:
			c.paper_count = mongo_get_objects(UploadRecord, corpus=c.pk).count()
			if c.pk == selected_cid:
				c.selected = True
	page_size = 10
	page_nums_list = [i for i in range(1,(len(clist)-1)/page_size+2)]
	return render(request, 'profile/profile.html', {'menu_index': 2, 'clist': clist, 'page_size': page_size, 'page_nums_list': page_nums_list})
	#data = serializers.serialize('json', clist, fields=('pk', 'name','description', 'ispublic', 'date_created'))
	#return make_response(content=json.dumps({ 'd': data }), content_type='application/json')


@login_required
def field_select_view(request):
	profile = mongo_get_object(UserProfile, pk=request.user.pk)
	ofid = profile['field'] if profile and 'field' in profile else None
	saved = False
	if request.method == 'POST':
		form = FieldSelectForm(request.POST)
		if form.is_valid():
			fid = form.cleaned_data['choice']
			if not profile:	# create new profile
				profile = {'_id': request.user.pk}
			if ofid != fid:	# need to update fid & cids
				profile['field'] = fid
				# TODO: db.venues.find()
				db = settings.DBC.common
				profile['pub_corpora'] = [c['_id'] for c in db.corpora.find({'field': fid, 'status': 2}, {'_id': 1})]
				mongo_save(UserProfile, **profile)
			saved = True	# saved successfully
			# return redirect(reverse('field_select'))
	else:
		form = FieldSelectForm(initial={'choice': ofid})
	return render(request, "profile/field_select.html", {'form': form, 'menu_index': 1, 'saved': saved})


@login_required
def corpus_view(request, cid):
	if request.method == 'GET':
		# show list of papers in corpus
		if request.user.is_superuser:
			corpus = mongo_get_object_or_404(Corpus, pk=cid)
		else:
			cid = int(cid)
			corpus = get_object_or_404(UserCorpus, pk=cid, user=request.user.pk)
		# plist = UploadRecord.objects.filter(corpus=corpus).order_by('date_added')
		plist = list(mongo_get_objects(UploadRecord, corpus=cid))
		if not request.user.is_superuser:
			for p in plist:
				p['timestamp'] = p['_id'].generation_time
				p['file'] = mongo_get_object(UploadFile, pk=p['file'])
		page_size = 10
		page_nums_list=[i for i in range(1, (len(plist)-1)/page_size+2)]
		return render(request, 'profile/corpus.html', {'c': corpus, 'plist': plist, 'menu_index': 2, 'page_size': page_size, 'page_nums_list': page_nums_list})
	# elif request.method == 'POST':
	#	 return redirect(reverse('corpus', args=[corpus.pk]))


@login_required
def corpus_update_view(request, cid):
	if not cid: #create
		if request.method == 'POST':
			form = CorpusForm(request.POST)
			if form.is_valid():
				# corpus = {'user': request.user.pk, 'name': form.cleaned_data['name'], 'description': form.cleaned_data['description']}
				# ocid = UserCorpus.objects.save(corpus)
				corpus = form.save(commit=False)
				corpus.user = request.user
				corpus.save()
				return redirect(reverse('corpus', args=[corpus.pk]))
		else:
			form = CorpusForm()
		return render(request, 'profile/corpus_update.html', {'form': form, 'menu_index': 2})
	else:   #update or delete
		corpus = get_object_or_404(UserCorpus, pk=cid, user=request.user.pk)
		print corpus
		if request.method == 'POST':
			form = CorpusForm(request.POST)
			if form.is_valid():
				corpus.name = form.cleaned_data['name']
				corpus.description = form.cleaned_data['description']
				corpus.save()
				return redirect(reverse('profile'))
		elif request.method == 'DELETE':
			# # TODO: use transaction
			# UploadRecord.objects.filter(corpus=corpus).delete()
			# corpus.delete()
			# #TODO delay deletion
			return make_response(content=json.dumps({ 'success': False }))
		else:
			form = CorpusForm(instance=corpus)
		return render(request, 'profile/corpus_update.html', {'form': form, 'menu_index': 2})


@login_required
def update_paper_view(request, cid, pid):
	raise Exception('Not implemented')
	# corpus = get_object_or_404(Corpus, pk=cid, user=request.user)
	# paper = get_object_or_404(UploadRecord, pk=pid, corpus=corpus)
	# if request.method == 'POST':
	# 	form = UploadRecordForm(request.POST)
	# 	if form.is_valid():
	# 		paper.title = form.cleaned_data['title']
	# 		# paper.author = form.cleaned_data['author']
	# 		# paper.source = form.cleaned_data['source']
	# 		paper.save()
	# 		return redirect(reverse('corpus', args=[corpus.pk]))
	# else:
	# 	form = UploadRecordForm(instance=paper)
	# return render(request, 'profile/update_paper.html', {'form': form, 'c': corpus, 'menu_index':1})


from django.db import transaction
from corpus_building.tasks import build_task

@login_required
def activate_view(request, cid):
	if request.method == 'POST':
		cid = int(cid)
		with transaction.atomic():
			corpus = get_object_or_404(UserCorpus, pk=cid, user=request.user)
			if corpus.status == 0:
				corpus.status = 1
				corpus.save()
				if settings.DEBUG:
					build_task(cid)
				else:
					build_task.delay(cid)
		profile = mongo_get_object(UserProfile, pk=request.user.pk)
		profile['pri_corpus'] = cid
		mongo_save(UserProfile, **profile)
		return redirect(reverse('profile'))
