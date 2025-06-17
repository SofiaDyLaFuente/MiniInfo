from django.contrib import admin
from indicador.models import PalavraChave, Categoria, Indicador, FonteExterna


@admin.register(FonteExterna)
class FonteExternaAdmin(admin.ModelAdmin):
    list_display = ["id", "descricao"]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nome"]

@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = [
        'categoria',
        'nome',
        'destaque',
        'ultima_atualizacao',
        'responsavel_tecnico'
    ]
    
    search_fields = ['nome']

    # Função para inserir automaticamente a pessoa que atualizou
    def save_model(self, request, obj, form, change):
        obj.responsavel_tecnico = request.user
        super().save_model(request, obj, form, change)

    
