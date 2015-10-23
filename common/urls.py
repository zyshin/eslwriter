from django.conf.urls import patterns, url
# from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

from registration.backends.default.views import RegistrationView
from common.forms import RegistrationFormUniqueEmailTermsOfService, SetPasswordFormValidate, PasswordChangeFormValidate


urlpatterns = patterns('',
	url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmailTermsOfService), name='registration_register'),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
)

urlpatterns += patterns('django.contrib.auth.views',
	url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', 'password_reset_confirm',
		{'post_reset_redirect': reverse_lazy('auth_password_reset_complete'), 'set_password_form': SetPasswordFormValidate},
		name='auth_password_reset_confirm'),
	url(r'^accounts/password/change/$', 'password_change',
		{'post_change_redirect': reverse_lazy('auth_password_change_done'), 'password_change_form': PasswordChangeFormValidate},
		name='auth_password_change'),
)

urlpatterns += patterns('common.views',
	url(r'^accounts/field/$', 'field_select_view', name='field_select'),

	url(r'^accounts/$', 'field_select_view', name='account'),
	url(r'^accounts/corpus/$', 'profile_view', name='profile'),
	url(r'^accounts/corpus/update/(?:(?P<cid>[^\s/]+?)/)?$', 'corpus_update_view', name='corpus_update'),
	url(r'^accounts/corpus/(?P<cid>[^\s/]+?)/$', 'corpus_view', name='corpus'),
	# url(r'^accounts/corpus/update/(?P<cid>\d+)/(?:(?P<pid>\d+)/)?$', 'update_paper_view', name='update_paper'),
	url(r'^accounts/corpus/activate/(?:(?P<cid>[^\s/]+?)/)?$', 'activate_view', name='activate'),
	#url(r'^accounts/corpus/new/$', 'new_corpus_view', name='create_corpus'),
	#url(r'^accounts/corpus/(?P<cid>\d+)/paper/(?P<pid>\S+)/$', 'paper_view', name='paper'),
)
