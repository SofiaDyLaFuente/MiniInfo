"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from config.settings import DEBUG
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

urlpatterns = [
    #Rota padrão para o painel de administração do Django
    path('admin/', admin.site.urls),
    # Inclui urls de autenticação fornecidas pelo django. Exclusivo do ambiente de deburação (frontend não usa essa url)
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Ponte para o arquivo de urls local
    path('api/v1/indicador/', include('indicador.urls')),
    # Vem da biblioteca simplejwt.views. Angular utiliza para se autenticar 
    path('api/v1/login/', TokenObtainPairView.as_view(), name='token_obtain_pair')
]

if DEBUG:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns