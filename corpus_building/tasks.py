from __future__ import absolute_import

from celery import shared_task
import gc
from common.models import UserCorpus
from .build import build_corpus


@shared_task(ignore_result=True)
def build_task(cid, *args, **kwargs):
	build_corpus(cid, *args, **kwargs)
	corpus = UserCorpus.objects.get(pk=cid)
	corpus.status = 2
	corpus.save()
	gc.collect()
	return True
