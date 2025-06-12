from rest_framework import viewsets
from .models import Indicador
from .serializers import IndicadorSerializer, IndicadorCreateUpdateSerializer
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

class IndicadorViewSet(viewsets.ModelViewSet):
    
    # 1. PERMISSÕES E QUERYSET OTIMIZADA
    permission_classes = [IsAuthenticated]
    queryset = Indicador.objects.select_related(
        'responsavel_tecnico'
    ).prefetch_related(
        'palavras_chave', 'etiquetas'
    ).order_by('-id')

    # 2. HABILITANDO OS MÉTODOS HTTP
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    # 3. FILTROS E ORDENAÇÃO
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['nome', 'ultima_atualizacao']
    search_fields = ['nome', 'conceito']

    # 4. MÉTODOS DE CUSTOMIZAÇÃO (O JEITO CERTO)
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IndicadorCreateUpdateSerializer
        return IndicadorSerializer

    def perform_create(self, serializer):
        serializer.save(atualizado_por=self.request.user)

    def perform_update(self, serializer):
        serializer.save(atualizado_por=self.request.user)