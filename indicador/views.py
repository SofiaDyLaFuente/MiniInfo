from rest_framework import viewsets
from .models import Indicador
from .serializers import IndicadorSerializer, IndicadorCreateUpdateSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
import json

class IndicadorViewSet(viewsets.ModelViewSet):
    
    # 1. PERMISSÕES E QUERYSET OTIMIZADA
    permission_classes = [IsAuthenticated]
    queryset = Indicador.objects.select_related(
        'responsavel_tecnico'
    ).prefetch_related(
        'palavras_chave', 'categoria'
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
        serializer.save(responsavel_tecnico=self.request.user)

    def perform_update(self, serializer):
        serializer.save(responsavel_tecnico=self.request.user)

    def retrieve(self, request, pk=None):

        try: 
            indicador = Indicador.objects.prefetch_related().get(id=pk)
            return Response(indicador, status.HTTP_200_OK)
        
        except ObjectDoesNotExist as e:
            return Response({}, status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        
        nome_filtro = request.GET.get('nome')
    
        try:
            with open('indicadores.json', 'r', encoding='utf-8') as f:
                dados = json.load(f)
                
                if nome_filtro:
                    resultados_filtrados = [
                        item for item in dados['results'] 
                        if nome_filtro.lower() in item['nome'].lower()
                    ]
                else:
                    resultados_filtrados = dados['results']
                
                return JsonResponse({"results": resultados_filtrados})



