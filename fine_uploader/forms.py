import os

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .utils import ispdf
from bson.objectid import ObjectId


class UploadFileForm(forms.Form):
	""" This form represents a basic request from Fine Uploader.
	The required fields will **always** be sent, the other fields are optional
	based on your setup.

	Edit this if you want to add custom parameters in the body of the POST
	request.
	"""
	qquuid = forms.CharField()
	qqfilename = forms.CharField()
	qqpartindex = forms.IntegerField(required=False)
	qqchunksize = forms.IntegerField(required=False)
	qqpartbyteoffset = forms.IntegerField(required=False)
	qqtotalfilesize = forms.IntegerField(required=False)
	qqtotalparts = forms.IntegerField(required=False)
	#author = forms.CharField(required=False)
	#source = forms.CharField(required=False)
	qqfile = forms.FileField()	# TODO: validate FileField

	def _clean_size(self, size):
		if size > settings.MAX_UPLOAD_SIZE:
			raise forms.ValidationError(_('File too large.'))
		if size == 0:
			raise forms.ValidationError(_('File too small.'))
		return size

	def clean_qquuid(self):
		uuid = self.cleaned_data['qquuid']
		try:
			ObjectId(uuid)
		except:
			raise forms.ValidationError(_('Invalid qquuid.'))
		return uuid

	def clean_qqtotalfilesize(self):
		size = self.cleaned_data['qqtotalfilesize']
		return self._clean_size(size)

	def clean_qqfilename(self):
		name = self.cleaned_data['qqfilename']
		if os.path.splitext(name)[1] != '.pdf':
			raise forms.ValidationError(_('Invalid file format.'))
		return name

	def clean_qqfile(self):
		f = self.cleaned_data['qqfile']
		if self._clean_size(f.size) != self.cleaned_data['qqtotalfilesize']:
			raise forms.ValidationError(_('Size does not match: qqtotalfilesize, f.size.'))
		if not ispdf(f):
			raise forms.ValidationError(_('File not valid PDF.'))
		return f
