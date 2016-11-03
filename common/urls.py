from django.conf.urls import url
# from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse_lazy

from registration.backends.default.views import RegistrationView
from common.forms import RegistrationFormUniqueEmailTermsOfService, SetPasswordFormValidate, PasswordChangeFormValidate

urlpatterns = []

urlpatterns += [
	url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmailTermsOfService), name='registration_register'),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
]

from django.contrib.auth import views as auth_views
urlpatterns += [
	url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm,
		{'post_reset_redirect': reverse_lazy('auth_password_reset_complete'), 'set_password_form': SetPasswordFormValidate},
		name='auth_password_reset_confirm'),
	url(r'^accounts/password/change/$', auth_views.password_change,
		{'post_change_redirect': reverse_lazy('auth_password_change_done'), 'password_change_form': PasswordChangeFormValidate},
		name='auth_password_change'),
]

from common import views as common_views
urlpatterns += [
	url(r'^accounts/field/$', common_views.field_select_view, name='field_select'),

	url(r'^accounts/$', common_views.field_select_view, name='account'),
	url(r'^accounts/corpus/$', common_views.profile_view, name='profile'),
	url(r'^accounts/corpus/update/(?:(?P<cid>[^\s/]+?)/)?$', common_views.corpus_update_view, name='corpus_update'),
	url(r'^accounts/corpus/(?P<cid>[^\s/]+?)/$', common_views.corpus_view, name='corpus'),
	# url(r'^accounts/corpus/update/(?P<cid>\d+)/(?:(?P<pid>\d+)/)?$', common_views.update_paper_view, name='update_paper'),
	url(r'^accounts/corpus/activate/(?:(?P<cid>[^\s/]+?)/)?$', common_views.activate_view, name='activate'),
	#url(r'^accounts/corpus/new/$', common_views.new_corpus_view, name='create_corpus'),
	#url(r'^accounts/corpus/(?P<cid>\d+)/paper/(?P<pid>\S+)/$', common_views.paper_view, name='paper'),
]
