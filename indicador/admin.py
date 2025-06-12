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
        'nome',
        'destaque',
        'ultima_atualizacao',
        'atualizado_por'
    ]

    filter_horizontal= ('palavras_chave', 'etiquetas')

    search_fields = ('nome', 'conceito', 'responsavel_tecnico')

    # Função para inserir automaticamente a pessoa que atualizou
    def save_model(self, request, obj, form, change):
        obj.atualizado_por = request.user
        super().save_model(request, obj, form, change)

    
