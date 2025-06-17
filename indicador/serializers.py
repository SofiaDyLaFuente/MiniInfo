from rest_framework import serializers
from .models import PalavraChave, Categoria, Indicador, FonteExterna
from django.contrib.auth import get_user_model

# Útil para pegar o modelo de usuário ativo no projeto
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups' ]

class FonteExternaSerialzier(serializers.ModelSerializer):
    class Meta:
        model = FonteExterna
        fields = ['id']


class PalavraChaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PalavraChave
        fields = ['id', 'nome', 'descricao']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']


class IndicadorSerializer(serializers.ModelSerializer):
    palavras_chave = PalavraChaveSerializer(many=True)
    categoria = CategoriaSerializer(many=True)
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
            'categoria',
            'conceito',
            'metodo_de_calculo',
            'interpretacao',
            'fonte_externa'
        ]
        read_only_fields = ['criado_em', 'ultima_atualizacao', 'responsavel_tecnico']

class IndicadorCreateUpdateSerializer(serializers.ModelSerializer):
    palavras_chave = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PalavraChave.objects.all()
    )
    categoria = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Categoria.objects.all(), required=False
    )
    class Meta:
        model = Indicador
        fields = [
            'nome', 'destaque', 'qualificacao', 'periodicidade', 'conceito',
            'metodo_de_calculo', 'interpretacao', 'palavras_chave', 'categoria'
        ]

    def create(self, validated_data):
        palavras_chave_data = validated_data.pop('palavras_chave')
        categoria_data = validated_data.pop('categoria', [])

        indicador = Indicador.objects.create(**validated_data)

        indicador.palavras_chave.set(palavras_chave_data)
        indicador.categoria.set(categoria_data)
        return indicador
    
    def update(self, instance, validated_data):
        palavras_chave_data = validated_data.pop('palavras_chave', None)
        categoria_data = validated_data.pop('categoria', None)

        # Usamos super().update() para atualizar os campos simples.
        instance = super().update(instance, validated_data)

        if palavras_chave_data is not None:
            instance.palavras_chave.set(palavras_chave_data)
        if categoria_data is not None:
            instance.categoria.set(categoria_data)

        return instance
    
class IndicadorListSerialzier(serializers.ModelSerializer):

    def listTodosIndicador(self):

        indicador = Indicador.objects.all()
        return indicador