from django import forms
from django.utils.translation import ugettext as _


class MensajeForm(forms.Form):
    imagen = forms.ImageField()
    mensaje = forms.CharField(label='Mensaje', max_length=100)

    def __init__(self, *args, **kwargs):
        super(MensajeForm, self).__init__(*args, **kwargs)

        self.fields['imagen'].widget.attrs.update({'ng-model': 'formData.imagen'})
        self.fields['mensaje'].widget.attrs.update({'ng-model': 'formData.mensaje'})
        self.fields['mensaje'].widget.attrs.update({'class': 'write_msg'})
        self.fields['mensaje'].widget.attrs.update({'placeholder': _('Escribe un mensaje')})
