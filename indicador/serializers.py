from rest_framework import serializers
from .models import PalavraChave, Etiqueta, Indicador
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PalavraChaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalavraChave
        fields = ['id', 'nome']


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ['id', 'nome']


class IndicadorSerializer(serializers.ModelSerializer):
    atualizado_por = UserSerializer(read_only=True)
    responsavel_tecnico = UserSerializer(read_only=True)
    palavra_chave = PalavraChaveSerializer(many=True)
    etiqueta = EtiquetaSerializer(many=True)
    qualificacao = serializers.ChoiceField(choices=Indicador.QUALIFICACAO_CHOICES)
    periodicidade = serializers.ChoiceField(choices=Indicador.PERIODICIDADE_CHOICES)
    
    class Meta:
        model = Indicador
        fields = [
            'id',
            'nome',
            'atualizado_por',
            'destaque',
            'criado_em',
            'ultima_atualizacao',
            'qualificacao',
            'periodicidade',
            'palavra_chave',
            'responsavel_tecnico',
            'etiqueta',
            'conceito',
            'metodo_de_calculo',
            'interpretacao'
        ]
        read_only_fields = ['criado_em', 'ultima_atualizacao', 'atualizado_por']

class IndicadorCreateSerializer(serializers.ModelSerializer):
    # Serializer para criação que aceita IDs para relações
   # palavra_chave = serializers.PrimaryKeyRelatedField(
   #     many=True, 
    #    queryset=PalavraChave.objects.all()
    #)
    #etiqueta = serializers.PrimaryKeyRelatedField(
    #    many=True, 
    #    queryset=Etiqueta.objects.all()
   # )
    
    class Meta:
        model = Indicador
        fields = [
            'nome',
            'destaque',
            'conceito',
            'metodo_de_calculo',
            'interpretacao'
        ]