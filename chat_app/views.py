__author__ = 'lorenzo'
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from chat_app.models import *
import pusher


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.cleaned_data['user']
            return HttpResponseRedirect("/chat/")
    else:
        form = LoginForm()
    return render(request, "chat_app/login.html", {
        'form': form
    })


def chat(request):
    # Variable declaration
    """

    :param request:
    :return:
    """
    user = request.session['user']
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    channel = 'public_test'
    event = 'msg'
    chat_field = '' # TODO variable to store previous messages, not working
    # GET vs POST
    if request.method == 'POST':
        # print("post")
        # if request.is_ajax():
        #     print("ajax")

        msg = request.POST.get("msg")
        loc_user = request.get('user')
        p = pusher.Pusher(
            app_id=app_key,
            key=key,
            secret=secret
        )
        print(loc_user)
        print(msg)
        p[channel].trigger(event, {"user": loc_user, "msg": msg})
            # ratings = Bewertung.objects.order_by(sortid)
            # locations = Location.objects.filter(locations_bewertung__in=ratings)
            # t = loader.get_template('result-page.html')
            # c = Context({ 'locs': locations })
        return HttpResponse("=>sended")
        # return HttpResponse("nope")

        # form = MsgForm(request.POST)
        # if form.is_valid():
        #     msg = form.cleaned_data['write_your_message']
        #     p = pusher.Pusher(
        #         app_id=app_key,
        #         key=key,
        #         secret=secret
        #     )
        #     p[channel].trigger(event, {"user": user, "msg": msg})

            # TODO it's to be changed as it reload completely the web-page deleting displayed messages.
            #      Different options under comments


            # Manually generate the new page
            # response = HttpResponse()
            # response.write(chat_field)
            # response.write(user + " said: " + msg + "<br/>")
            # return response

            # Reload the template /chat/
            # return HttpResponseRedirect("/chat/")

            # return render(request, "chat_app/chat.html", {
            # 'user': user,
            # 'app_key': app_key,
            # 'key': key,
            # 'channel' : channel,
            # 'event' : event,
            # 'form' : form,
            # })

    else:
        form = MsgForm()
        return render(request, "chat_app/chat.html", {
            'user': user,
            'app_key': app_key,
            'key': key,
            'channel': channel,
            'event': event,
            'form': form,
            'chat_field' : chat_field
        })


def chat_send(request):
    # Variable declaration
    """

    :param request:
    :return:
    """
    user = request.session['user']
    app_key = "55129"
    key = 'f073ebb6f5d1b918e59e'
    secret = '360b346d88ee47d4c230'
    channel = 'public_test'
    event = 'msg'

    # print("chat_send working")
    msg = request.GET.get('msg')
    p = pusher.Pusher(
        app_id=app_key,
        key=key,
        secret=secret
    )
    p[channel].trigger(event, {"user": user, "msg": msg})
    return HttpResponse(msg)