from django.db import models
from django.conf import settings

class LogModel(models.Model):
 
    criado_em = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True