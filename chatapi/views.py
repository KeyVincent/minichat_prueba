import json

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from chatapi.models import Mensaje
from .form import MensajeForm

@login_required
def index(request):
    form = MensajeForm()
    return render(request, 'chat_principal/chat_principal.html', {'form': form})

@login_required
def save(request):
    if request.is_ajax():
        if 'multipart/form-data' not in str(request.META.get('CONTENT_TYPE', '')):
            request.POST = json.loads(request.body.decode('utf-8'))
    mensaje = Mensaje()
    posted_files = None
    if request.FILES:
        posted_files = request.FILES
    mensaje.mensaje = request.POST.get('mensaje')
    mensaje.usuario = request.user
    if posted_files:
        mensaje.imagen_archivo = posted_files.get('imagen')
    mensaje.save()

    res = {'success': True, 'id': mensaje.id}
    return HttpResponse(json.dumps(res))
