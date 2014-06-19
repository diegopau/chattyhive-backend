# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from core.models import ChUser

from email_confirmation.models import EmailConfirmation, EmailChangePassword
from login.models import DoublePassForm


def confirm_email(request, confirmation_key):
    
    confirmation_key = confirmation_key.lower()
    email_address = EmailConfirmation.objects.confirm_email(confirmation_key)
    
    # return render_to_response("email_confirmation/confirm_email.html", {
    #     "email_address": email_address,
    # }, context_instance=RequestContext(request))
    return HttpResponseRedirect("/email_confirmed/")


def email_confirmed(request):
    return render(request, "email_confirmation/email_confirmed.html")


def email_warning(request):
    return render(request, "email_confirmation/email_warning.html")


def change_password(request, confirmation_key):
    if request.method == "GET":
        confirmation_key = confirmation_key.lower()
        EmailChangePassword.objects.change_pass(confirmation_key)
        user = EmailChangePassword.objects.get(confirmation_key=confirmation_key).email_address.user.user
        form = DoublePassForm()
        request.session['user'] = user.username
        return render(request, "login/change_pass.html", {
            'form': form,
            'user': user.username
        })
    elif request.method == "POST":
        user = ChUser.objects.get(username=confirmation_key)
        form = DoublePassForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponse("Your password has been changed")


def password_changed(request):
    if request.method == "POST":
        form = DoublePassForm(request.POST)
        if form.is_valid():
            user = ChUser.objects.get(username=request.session['user'])
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponse("Your password has been changed")


    # return HttpResponseRedirect("/change_pass/")