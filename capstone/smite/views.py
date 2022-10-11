from smite.models import Skin, Session, God
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
import requests
import hashlib
import json
with open('hide.json') as f:
    data = json.load(f)
dev_id = data['DEV_ID']
auth_key = data['AUTH_KEY']

# Create your views here.
date_utc = datetime.utcnow()
date = date_utc.strftime('%Y%m%d%H%M%S')


def index(request):
    session_id = Session.objects.get(getter_id=1)
    print('sess id', session_id)
    signature = f'{dev_id}testsession{auth_key}{date}'
    signature_hashed = hashlib.md5(signature.encode()).hexdigest()
    test_response = requests.get(
        f'https://api.smitegame.com/smiteapi.svc/testsessionjson/{dev_id}/{signature_hashed}/{session_id}/{date}').json()

    if (test_response.startswith('Invalid session id')):
        print('created session')
        signature = f'{dev_id}createsession{auth_key}{date}'
        signature_hashed = hashlib.md5(signature.encode()).hexdigest()
        response = requests.get(
            f'https://api.smitegame.com/smiteapi.svc/createsessionjson/{dev_id}/{signature_hashed}/{date}').json()
        Session.objects.all().delete()
        sess = Session(getter_id=1, session_id=response['session_id'])
        sess.save()
        print(sess)

    else:
        response = test_response

    context = {'dev': dev_id, 'auth': auth_key,
               'hashed': signature_hashed, 'time': date, 'res': response, 'sess': session_id}
    return render(request, 'smite/index.html', context)


def gods(request):
    day = datetime.now()
    print(day.weekday(), day.hour, day.minute)
    session_id = Session.objects.get(getter_id=1)
    signature = f'{dev_id}getgods{auth_key}{date}'
    signature_hashed = hashlib.md5(signature.encode()).hexdigest()
    if day.weekday() == 4 and day.hour == 16 and day.minute == 46:
        God.objects.all().delete()
        response = requests.get(
            f'https://api.smitegame.com/smiteapi.svc/getgodsjson/{dev_id}/{signature_hashed}/{session_id}/{date}/1').json()
        save_response_to_gods = God(gods=response)
        save_response_to_gods.save()
    else:
        response = God.objects.first().gods

    context = {'gods': response, 'sess': session_id}
    return render(request, 'smite/gods.html', context)


def items(request):
    session_id = Session.objects.get(getter_id=1)
    signature = f'{dev_id}getitems{auth_key}{date}'
    signature_hashed = hashlib.md5(signature.encode()).hexdigest()
    response = requests.get(
        f'https://api.smitegame.com/smiteapi.svc/getitemsjson/{dev_id}/{signature_hashed}/{session_id}/{date}/1').json()
    context = {'res': response, 'sess': session_id}
    return render(request, 'smite/items.html', context)


def search_player(request):
    player = request.POST.get('player')
    return HttpResponseRedirect(reverse('smite:search_results', args=(player,)))


def search_results(request, player):
    session_id = Session.objects.get(getter_id=1)
    signature = f'{dev_id}searchplayers{auth_key}{date}'
    signature_hashed = hashlib.md5(signature.encode()).hexdigest()
    response = requests.get(
        f'https://api.smitegame.com/smiteapi.svc/searchplayersjson/{dev_id}/{signature_hashed}/{session_id}/{date}/{player}').json()

    context = {'player': response, 'sess': session_id}
    return render(request, 'smite/search_results.html', context)


def player(request, player, portal):
    session_id = Session.objects.get(getter_id=1)
    signature = f'{dev_id}getplayer{auth_key}{date}'
    signature_hashed = hashlib.md5(signature.encode()).hexdigest()
    response = requests.get(
        f'https://api.smitegame.com/smiteapi.svc/getplayerjson/{dev_id}/{signature_hashed}/{session_id}/{date}/{player}').json()
    print(player, portal, response)
    context = {'player': response[0], 'sess': session_id}
    return render(request, 'smite/player.html', context)


def god(request, r_Name):
    session_id = Session.objects.get(getter_id=1)
    gods = God.objects.first().gods
    god = {}
    for g in gods:
        if g['Name'] == r_Name:
            god = g
    context = {'res': gods[0], 'sess': session_id, 'god': god}
    return render(request, 'smite/god.html', context)
