# Eventex

Sistema de Eventos encomendado pela Morena

## Como desenvolver?

1. Instale o docker e docker-compose.
2. Configure o .env.
3. Execute os testes.

```console
git clone git@github.com:klasrak/eventex.git wttd
cd wttd
docker-compose up -d
docker-compose run app ./manage.py test
```
