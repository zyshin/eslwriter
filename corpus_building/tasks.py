from __future__ import absolute_import

from celery import shared_task
import gc
from common.models import UserCorpus
from .build import build_corpus


@shared_task(ignore_result=True)
def build_task(cid, *args, **kwargs):
	try:
		build_corpus(cid, *args, **kwargs)
		UserCorpus.objects.filter(pk=cid).update(status=2)
	except Exception as e:
		print '[Exception when building]', repr(e)
		UserCorpus.objects.filter(pk=cid).update(status=-2)
	gc.collect()
	return True
