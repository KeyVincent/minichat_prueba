from rest_framework import static, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Mensaje
from .serializers import ChatSerializer


class ChatAPI(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = Mensaje.objects.all().order_by('-fecha')
    pagination_class = PageNumberPagination

    @action(methods=['get'], detail=False, name="get_object")
    def get_object(self, request):
        pk = request.GET.get('pk')
        try:
            mensaje = Mensaje.objects.get(id=pk)
            serializer = ChatSerializer(mensaje)
            return Response(serializer.data)
        except Mensaje.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    @action(methods=['get'], detail=False, name="delete")
    def delete(self, request):
        pk = request.GET.get('pk')
        mensaje = Mensaje.objects.get(id=pk)
        mensaje.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, name="delete")
    def new_messages(self, request):
        last_message_id = request.GET.get('last_message_id')
        return Response(data=Mensaje.objects.filter(id__gt=last_message_id).exists())

