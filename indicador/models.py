from django.db import models
from django.conf import settings


class PalavraChave(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta: 
        verbose_name = "palavra chave"
        verbose_name_plural = "palavras chave"


class Etiqueta(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True) 

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "etiqueta"
        verbose_name_plural = "etiquetas"


class Indicador(models.Model):

    QUALIFICACAO_CHOICES = (
        ("A", "1"),
        ("B", "2"),
    )

    PERIODICIDADE_CHOICES = (
        ("diariamente", "Diariamente"),
        ("semanalmente", "Semanalmente"),
        ("mensalmente", "Mensalmente"),
        ("anualmente", "Anualmente"),
        ("bianualmente", "Bianualmente"),
        ("a cada 3 anos", "A cada 3 anos"),
        ("a cada 5 anos", "A cada 5 anos"),
    )

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="atualizado_por", on_delete=models.CASCADE, editable=False
    )
    destaque = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    qualificacao = models.CharField(max_length=1, choices=QUALIFICACAO_CHOICES)
    periodicidade = models.CharField(max_length=20, choices=PERIODICIDADE_CHOICES)
    palavras_chave = models.ManyToManyField(PalavraChave, related_name="indicadores")
    responsavel_tecnico = models.CharField(max_length=255)
    etiquetas = models.ManyToManyField(Etiqueta, related_name="indicadores")
    conceito = models.TextField(max_length=500, blank=True)
    metodo_de_calculo = models.TextField(max_length=500, blank=True)
    interpretacao = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "indicador"
        verbose_name_plural = "indicadores"    
    



