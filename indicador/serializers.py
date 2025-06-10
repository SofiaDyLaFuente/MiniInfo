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

class IndicadorCreateUpdateSerializer(serializers.ModelSerializer):
    
    # Para relacionamentos, esperamos receber do front apenas ID
    responsavel_tecnico = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    palavra_chave = serializers.PrimaryKeyRelatedField(
        many=True, queryset=PalavraChave.objects.all()
    )
    etiqueta = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Etiqueta.objects.all()
    )
       
    #def create (self, validated_data):
        #return Indicador(**validated_data)    Fazer dessa forma so salva o objeto em memória, e não no banco 
    class Meta:
        model = Indicador
        
        # Fields contém os campos que devem ser enviados pelo frontend 
        fields = [
            'nome',
            'destaque',
            'qualificacao',
            'periodicidade',
            'conceito',
            'metodo_de_calculo',
            'interpretacao',
            'responsavel_tecnico',
            'palavra_chave',
            'etiqueta',
        ]

    def create(self, validated_data):
        # Campos de relacionamento manytomany precisam ser salvos depois do objeto ser criado
        # Faz o pop e insere posteriormente 
        palavra_chave_data = validated_data.pop('palavra_chave')
        etiqueta_data = validated_data.pop('etiqueta')

        indicador = Indicador.objects.create(**validated_data)
        indicador.palavra_chave.set(palavra_chave_data)
        indicador.etiqueta.set(etiqueta_data)
        # .set() já salva a relação ManyToMany, não é necessário chamar indicador.save() novamente

        return indicador
    
    
    # Revisar 
    def update(self, instance, validated_data):
        # Atualize os campos do objeto instance com os dados validados
        palavra_chave_data = validated_data.pop('palavra_chave', None)
        etiqueta_data = validated_data.pop('etiqueta', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if palavra_chave_data is not None:
            instance.palavra_chave.set(palavra_chave_data)
        if etiqueta_data is not None:
            instance.etiqueta.set(etiqueta_data)

        return instance