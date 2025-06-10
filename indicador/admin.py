from django.contrib import admin
from indicador.models import PalavraChave, Etiqueta, Indicador


@admin.register(PalavraChave)
class PalavraChaveAdmin(admin.ModelAdmin):
    list_display = ["nome"]

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ["nome"]

@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nome',
        'destaque',
        'criado_em',
        'ultima_atualizacao',
        'qualificacao',
        'periodicidade',
        'conceito',
        'metodo_de_calculo',
        'interpretacao'
    ]

    filter_horizontal= ('palavra_chave', 'etiqueta')
    
