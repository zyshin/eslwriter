from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from registration.models import RegistrationProfile

def send_mails(emails):
    settings.ACTIVATION_EMAIL_HTML = 'registration/activation_prompt_email.html'
    site = get_current_site(None)
    for email in emails:
        profile = RegistrationProfile.objects.get(user__email=email)
        RegistrationProfile.objects.resend_activation_mail(profile.user.email, site)
    del settings.ACTIVATION_EMAIL_HTML
