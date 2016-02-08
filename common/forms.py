from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm

from registration.users import UserModel
from registration.forms import RegistrationForm

from common.models import *


class RegistrationFormUniqueEmailTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service and enforces uniqueness of
    email addresses.
    """
    username = forms.EmailField(max_length=30, label=_("E-mail"))
    email = forms.EmailField(max_length=30, label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                min_length=6, max_length=30,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                min_length=6, max_length=30,
                                label=_("Password (again)"))
    tos = forms.BooleanField(widget=forms.CheckboxInput,
                             help_text=_('I have read and agree to the'),
                             error_messages={'required': _("You must agree to the terms")})

    def __init__(self, *args, **kwargs):
        query_dict = kwargs.get('data')
        if query_dict:
            query_dict = query_dict.copy()
            query_dict.update({'username': query_dict.get('email')})
            kwargs.update({'data': query_dict})
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if UserModel().objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class SetPasswordFormValidate(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"),
                                    min_length=6, max_length=30,
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    min_length=6, max_length=30,
                                    widget=forms.PasswordInput)


class PasswordChangeFormValidate(SetPasswordFormValidate, PasswordChangeForm):
    pass


class CorpusForm(forms.ModelForm):
    class Meta:
        model = UserCorpus
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 3,'class':'form-control'}),
            'name':forms.TextInput({'class':'form-control'})
        }
        help_texts = {
            'name': _('Name of your corpus.'),
            'description': _('Description of your corpus.'),
        }
        error_messages = {
            'name': {
                'max_length': _("This corpus name is too long."),
            },
        }
    # name = forms.CharField(max_length=30)
    # description = forms.CharField(max_length=150)


# class UploadRecordForm(forms.ModelForm):
#     class Meta:
#         # model = UploadRecord
#         fields = ['title']
#         widgets={
#             'title':forms.TextInput({'class':'form-control'})
#         }
#         help_texts = {
#             'title': _('Actual title of this paper.'),
#             # 'author': _('e.g. <i>A. Hanks; Darly N.G.</i> (Separated by <b>;</b>)'),
#             # 'source': _('Where does this paper come from?'),
#         }
#         error_messages = {
#             'title': {
#                 'max_length': _("This title is too long."),
#             },
#         }


class FieldSelectForm(forms.Form):
    choice = forms.ChoiceField(widget=forms.Select, 
                               label=_('Choose your interested field'),
                               error_messages={'required': _("You must choose one field from the list"), 
                                               'invalid_choice': _("You must choose one field from the list")})

    def __init__(self, *args, **kwargs):
        super(FieldSelectForm, self).__init__(*args, **kwargs)
        _pipeline = [{'$group': {'_id': '$domain', 'fields': {'$push': {'i': '$_id', 'name': '$name'}}}}]
        choices = [(d['_id'], [(int(f['i']), f['name']) for f in d['fields']]) for d in settings.DBC.esl.fields.aggregate(_pipeline)]
        choices.insert(0, (None, '------------ Choose one field ------------'))
        choices.append(('Other fields to be added', ()))
        self.fields['choice'].choices = choices

    def clean_choice(self):
        c = self.cleaned_data['choice']
        try:
            c = int(c)
        except:
            raise forms.ValidationError(_("Field id is not a valid number."))
        return c
