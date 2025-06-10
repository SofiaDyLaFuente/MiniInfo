from rest_framework.routers import SimpleRouter
from .views import IndicadorViewSet

# Com o uso use_regex_path instruimos o Django a usar o path() ao invés do obsoleto re_path() (Boas práticas)
# Simple route = Classe do DRF que gera automaticamente as rotas para um viewset
# Como usamos trailing_slash = True obrigatoriamente a url global precisa ter barra no final
router = SimpleRouter(trailing_slash=True, use_regex_path=False)

# Método que conecta as urls ao viewset e gera automaticamente as rotas com base nas ações que ele encontrar
router.register("", viewset=IndicadorViewSet, basename="indicador")

# urlpatterns é a váriavel que o Django procura em cada arquivo urls.py para gerar as urls
urlpatterns = router.urls