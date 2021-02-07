from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext as _

User = get_user_model()

class Mensaje(models.Model):
    usuario = models.ForeignKey(User, verbose_name=_("Usuario"), blank=True, db_index=True, null=True, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha'))
    imagen_archivo = models.ImageField(upload_to='images', null=True, blank=True, verbose_name=_("Imagen"))
    mensaje = models.TextField(null=True, blank=True, verbose_name=_("Mensaje"))
