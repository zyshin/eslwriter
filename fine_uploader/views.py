import json
import logging
import os
import shutil
import hashlib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from bson.objectid import ObjectId

from common.models import UserCorpus
from common.utils import *
from .forms import UploadFileForm
from . import utils
from corpus_building.refine import refine


# logger = logging.getLogger('django')


class UploadView(View):
	""" View which will handle all upload requests sent by Fine Uploader.
	See: https://docs.djangoproject.com/en/dev/topics/security/#user-uploaded-content-security

	Handles POST and DELETE requests.
	"""
	# @method_decorator(login_required)
	@csrf_exempt
	def dispatch(self, *args, **kwargs):
		request = args[0]
		cid = int(kwargs.get('cid', '0'))
		corpus = get_object_or_404(UserCorpus, pk=cid, user=request.user.pk)
		kwargs['corpus'] = corpus
		return super(UploadView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		corpus = kwargs.get('corpus')
		# pid = kwargs.get('pid')
		# if pid: #paper_view
			# pass
			# paper = get_object_or_404(UploadRecord, pk=pid, corpus=corpus)
			# dest_folder = os.path.join(settings.UPLOAD_DIR, paper.qquuid)
			# dest = os.path.join(dest_folder, 'refined2.txt')
			# if not os.path.isfile(dest):
			#	dest = os.path.join(dest_folder, 'content.txt')
			# if not os.path.isfile(dest):
			#	return make_response(status=404)
			# return make_response(content=file(dest, 'r').read())
		# else:   #upload_view
		return render(request, 'fine_uploader/upload.html', {'c': corpus, 'menu_index': 2})

	def post(self, request, *args, **kwargs):
		"""A POST request. Validate the form and then handle the upload
		based ont the POSTed data. Does not handle extra parameters yet.
		"""
		form = UploadFileForm(request.POST, request.FILES)
		corpus = kwargs.get('corpus')
		if form.is_valid() and corpus and corpus.status != 1:
			handle_upload(corpus, request.FILES['qqfile'], form.cleaned_data)
			corpus.status = 0
			corpus.save()
			return make_response(content=json.dumps({ 'success': True }))
		else:
			return make_response(status=400,
				content=json.dumps({
					'success': False,
					'error': '%s' % repr(form.errors)
				}))

	def delete(self, request, *args, **kwargs):
		"""A DELETE request. If found, deletes a file with the corresponding
		UUID from the server's filesystem.
		"""
		qquuid = kwargs.get('qquuid')
		corpus = kwargs.get('corpus')
		if qquuid and corpus and corpus.status != 1:
			try:
				handle_deleted_file(qquuid)
				return make_response(content=json.dumps({ 'success': True }))
			except Exception, e:
				return make_response(status=400,
					content=json.dumps({
						'success': False,
						'error': '%s' % repr(e)
					}))
		return make_response(status=404,
			content=json.dumps({
				'success': False,
				'error': 'File not present'
			}))


@timeit
def handle_upload(corpus, f, fileattrs):
	""" Handle a chunked or non-chunked upload.
	"""
	# logger.info(fileattrs)

	# dest_folder = os.path.join(settings.UPLOAD_DIR, fileattrs['qquuid'])
	# dest = os.path.join(dest_folder, fileattrs['qqfilename'])
	qqtotalparts = int(fileattrs['qqtotalparts'] or 1)
	qqpartindex = int(fileattrs['qqpartindex'] or 0)

	# # Chunked
	# if qqtotalparts > 1:
	# 	dest_folder = os.path.join(settings.CHUNKS_DIR, fileattrs['qquuid'])
	# 	dest = os.path.join(dest_folder, fileattrs['qqfilename'], str(qqpartindex))
	# 	# logger.info('Chunked upload received')

	f.seek(0)
	md5 = hashlib.md5(f.read()).hexdigest()
	f.seek(0)
	qquuid = fileattrs['qquuid']
	key = {'size': f.size, 'md5': md5}
	file_record = {'_id': ObjectId(qquuid), 'status': 0, 'nwords': 0}
	file_record.update(key)
	old_record = settings.DBC.common.files.find_one_and_update(key, {'$setOnInsert': file_record}, upsert=True)
	if not old_record:
		paper_dest = paper_path(qquuid)
		utils.save_upload(f, paper_dest)
		extractedResult = utils.extracted(paper_dest) # extract
		if extractedResult:
			with open(extracted_path(qquuid), 'w') as fout:
				fout.write(extractedResult)
			refinedResult = refine(extractedResult) # refine
			if refinedResult:
				with open(refined_path(qquuid), 'w') as fout:
					fout.write(refinedResult)
				status = 2
			else:
				status = -2
		else:
			status = -1
		settings.DBC.common.files.find_one_and_update(file_record, {'$set': {'nwords': len(extractedResult.split()), 'status': status}})

	# logger.info('Upload saved: %s' % dest)

	# # If the last chunk has been sent, combine the parts.
	# if qqtotalparts > 1 and qqpartindex == (qqtotalparts - 1):

	# 	# logger.info('Combining chunks: %s' % os.path.dirname(dest))
	# 	utils.combine_chunks(qqtotalparts,
	# 		fileattrs['qqtotalfilesize'],
	# 		source_folder=os.path.dirname(dest),
	# 		dest=os.path.join(settings.UPLOAD_DIR, fileattrs['qquuid'], fileattrs['qqfilename']))
	# 	# logger.info('Combined: %s' % dest)

	# 	shutil.rmtree(os.path.dirname(os.path.dirname(dest)))

	# # Upload done.
	# if qqpartindex == (qqtotalparts - 1):
	# 	pass

	file_id = old_record and old_record['_id'] or ObjectId(qquuid)
	title = os.path.splitext(fileattrs['qqfilename'])[0]
	upload_record = {'file': file_id, 'corpus': corpus.pk, 'title': title}
	settings.DBC.common.uploads.insert_one(upload_record)


def handle_deleted_file(paper):
    """ Handles a filesystem delete based on UUID."""
    # settings.DBC.common.uploads.delete_one()
    # loc = os.path.join(settings.UPLOAD_DIR, uuid)
    # shutil.rmtree(loc)
