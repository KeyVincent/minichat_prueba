from rest_framework import serializers

from chatapi.models import Mensaje


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    usuario = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    usuario_username = serializers.ReadOnlyField(source='usuario.username')
    usuario_first_name = serializers.ReadOnlyField(source='usuario.first_name')
    usuario_last_name = serializers.ReadOnlyField(source='usuario.last_name')
    fecha = serializers.ReadOnlyField()
    mensaje = serializers.ReadOnlyField()
    imagen_archivo = serializers.FileField()

    class Meta:
        model = Mensaje
        fields = ('id', 'usuario', 'fecha', 'imagen_archivo',
                  'mensaje', 'usuario_username', 'usuario_first_name',
                  'usuario_last_name')
