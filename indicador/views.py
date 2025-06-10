from rest_framework import viewsets
from .models import Indicador
from .serializers import IndicadorSerializer, IndicadorCreateUpdateSerializer
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

class IndicadorViewSet(viewsets.ModelViewSet):

    http_method_names = ["get", "post", "put"]
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated]
    queryset = Indicador.objects.all()
    serializer_class = IndicadorSerializer
   
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IndicadorCreateUpdateSerializer
        return IndicadorSerializer
    
    def create(self, request):
        try: 
            body = request.data
            serializer = IndicadorCreateUpdateSerializer(data=body)
            
            if serializer.is_valid(raise_exception=True):
                indicador = serializer.save(atualizado_por=self.request.user)
                return Response({"id": indicador.id}, status.HTTP_201_CREATED)
        
        except ValidationError as e:
            return Response({"code": 400, "message": e}, status=400)
        except ObjectDoesNotExist as e:
            return Response({"code": 404, "message": str(e)}, status=404)

     



        


