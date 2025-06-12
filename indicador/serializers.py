from rest_framework import serializers
from .models import PalavraChave, Etiqueta, Indicador
from django.contrib.auth import get_user_model

# Útil para pegar o modelo de usuário ativo no projeto
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
    palavras_chave = PalavraChaveSerializer(many=True)
    etiquetas = EtiquetaSerializer(many=True)
    qualificacao = serializers.ChoiceField(choices=Indicador.QUALIFICACAO_CHOICES)
    periodicidade = serializers.ChoiceField(choices=Indicador.PERIODICIDADE_CHOICES)
    
    class Meta:
        model = Indicador
        fields = [
            'id',
            'nome',
            'destaque',
            'criado_em',
            'ultima_atualizacao',
            'qualificacao',
            'periodicidade',
            'palavras_chave',
            'responsavel_tecnico',
            'etiquetas',
            'conceito',
            'metodo_de_calculo',
            'interpretacao'
        ]
        read_only_fields = ['criado_em', 'ultima_atualizacao', 'atualizado_por']

class IndicadorCreateUpdateSerializer(serializers.ModelSerializer):
    palavras_chave = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PalavraChave.objects.all()
    )
    etiquetas = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Etiqueta.objects.all(), required=False
    )
    class Meta:
        model = Indicador
        fields = [
            'nome', 'destaque', 'qualificacao', 'periodicidade', 'conceito',
            'metodo_de_calculo', 'interpretacao', 'responsavel_tecnico',
            'palavras_chave', 'etiquetas'
        ]

    def create(self, validated_data):
        palavras_chave_data = validated_data.pop('palavras_chave')
        etiquetas_data = validated_data.pop('etiquetas', [])

        indicador = Indicador.objects.create(**validated_data)

        indicador.palavras_chave.set(palavras_chave_data)
        indicador.etiquetas.set(etiquetas_data)
        return indicador
    
    def update(self, instance, validated_data):
        palavras_chave_data = validated_data.pop('palavras_chave', None)
        etiquetas_data = validated_data.pop('etiquetas', None)

        # Usamos super().update() para atualizar os campos simples.
        instance = super().update(instance, validated_data)

        if palavras_chave_data is not None:
            instance.palavras_chave.set(palavras_chave_data)
        if etiquetas_data is not None:
            instance.etiquetas.set(etiquetas_data)

        return instance