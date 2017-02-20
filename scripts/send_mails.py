from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from registration.models import RegistrationProfile
from django.core.mail import EmailMultiAlternatives, send_mail
import time


def send_activation_prompt_emails(receivers):
    settings.ACTIVATION_EMAIL_HTML = 'registration/activation_prompt_email.html'
    site = get_current_site(None)
    for receiver in receivers:
        profile = RegistrationProfile.objects.get(user__email=receiver)
        RegistrationProfile.objects.resend_activation_mail(profile.user.email, site)
        time.sleep(500)
    del settings.ACTIVATION_EMAIL_HTML

def send_emails(subject, message_txt, message_html, receivers):
    from_email = getattr(settings, 'REGISTRATION_DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
    for receiver in receivers:
        send_mail(subject, message_txt, from_email, [receiver], html_message=message_html)
        time.sleep(500)
