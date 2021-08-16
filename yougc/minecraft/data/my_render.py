import json
from random import randint

from django.conf import settings
from django.shortcuts import render as django_render

from .meta import NOTIFICATION_CLASSES


def render(request, template, context, *args, **kwargs):
    messages = request.session.get('messages', [])
    if request.session.get('messages'):
        del request.session['messages']
    context['notification_messages'] = messages
    response = django_render(request, template, context, *args, **kwargs)
    response['Last-Modified'] = settings.LAST_MODIFIED
    return response


def set_message(request, message, skip=True, cls='', color=''):
    if not request.session.get('messages'):
        request.session['messages'] = []
    if cls:
        color, skip = NOTIFICATION_CLASSES[cls]
    elif not color:
        color, skip = NOTIFICATION_CLASSES['success']
    request.session['messages'].append([message, color, int(skip)])

    return request
