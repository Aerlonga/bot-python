# bot-python

## Como executar o projeto dentro do container

1. Acesse o container Docker:
   docker compose exec botcity bash

2. Ative o ambiente virtual:
   source /venv/bin/activate

3. Execute o bot (exemplo):
   python3 bot_simulado.py

---

## Como rodar os testes com coverage e gerar o relatório HTML

1. Rode os testes com coverage:
   coverage run test.py

2. Gere o relatório HTML:
   coverage html

3. O relatório será salvo na pasta `htmlcov`.

4. Para visualizar o relatório:

  Vá até a pasta `htmlcov` e abra o arquivo `index.html` com o navegador.

---
