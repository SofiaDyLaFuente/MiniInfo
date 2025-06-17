import uuid
from django.db import models
from django.conf import settings
from utils.models import LogModel
from taggit.managers import TaggableManager
from taggit.models import GenericTaggedItemBase, TagBase

# TODO: Corrigir a implementação da fonte externa 
class FonteExterna(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,      
        editable=False
    )
    descricao = models.TextField(max_length=500) 
    
    class Meta: 
        verbose_name = "fonte externa"


class PalavraChave(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta: 
        verbose_name = "palavra chave"
        verbose_name_plural = "palavras chave"


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True) 
    descricao = models.TextField(max_length=500)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"


class Indicador(LogModel):

    NEGATIVO = -1
    INDEFINIDO = 0
    POSITIVO = 1

    QUALIFICACAO_CHOICES = (            
        (NEGATIVO, "Negativo"),
        (INDEFINIDO, "Indefinido"),
        (POSITIVO, "Positivo")
    )

    MENSAL = 0
    BIMESTRAL = 1
    TRIMESTRAL = 2
    SEMESTRAL = 3
    ANUAL = 4
    
    PERIODICIDADE_CHOICES = (
        (MENSAL, "Mensal"),
        (BIMESTRAL, "Bimestral"),
        (TRIMESTRAL, "Trimestral"),
        (SEMESTRAL, "Semestral"),
        (ANUAL, "Anual")   
    )

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    responsavel_tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="responsavel_tecnico", on_delete=models.CASCADE, editable=False
    )
    destaque = models.BooleanField(default=False)
    qualificacao = models.SmallIntegerField(choices=QUALIFICACAO_CHOICES)
    periodicidade = models.SmallIntegerField(choices=PERIODICIDADE_CHOICES)
    conceito = models.TextField(max_length=500, blank=True)
    metodo_de_calculo = models.TextField(max_length=500, blank=True)
    interpretacao = models.TextField(max_length=500, blank=True)
    palavras_chave = TaggableManager(through='taggit.TaggedItem', to='PalavraChave', verbose_name='palavra chave')
    categoria = models.ForeignKey(Categoria, related_name="indicadores", blank=True, on_delete=models.CASCADE)
    fonte_externa = models.OneToOneField(FonteExterna, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "indicador"
        verbose_name_plural = "indicadores"    
    



