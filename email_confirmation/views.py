# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from email_confirmation.models import EmailConfirmation


def confirm_email(request, confirmation_key):
    
    confirmation_key = confirmation_key.lower()
    email_address = EmailConfirmation.objects.confirm_email(confirmation_key)
    
    # return render_to_response("email_confirmation/confirm_email.html", {
    #     "email_address": email_address,
    # }, context_instance=RequestContext(request))
    return HttpResponseRedirect("/email_confirmed/")


def email_confirmed(request):
    return render(request, "email_confirmation/email_confirmed.html")