#MiniInfoDf - Backend

Repositório para o backend do Mini InfoDF

## Instalação

Para executar o sistema, execute os passos abaixo:

1. Instale o Python no sistema;

2. Clone o repositório e acesse a pasta raiz;

```shell
git clone git remote add origin https://github.com/SofiaDyLaFuente/MiniInfo.git
cd MiniInfo
```

3. Crie um ambiente virtual e ative-o:

```shell
python -n venv venv
.\venv\Scripts\activate
```

4. Instale as dependências:

```shell
pip install -r requirements.txt
```

5. Execute as migrations:

```shell
python manage.py migrate
```

6. Execute o sistema em modo de desenvolvimento:

```shell
python manage.py runserver
```

O sistema estará acessível em [http:localhost:8000]