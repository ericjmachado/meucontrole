# Meu controle

Backend em Python

### Tecnologias empregadas

- Django v3.2 LTS
- Python 3.8.6 (https://askubuntu.com/questions/1261775/why-i-cant-install-python-3-8)
- virtualenv

## Como rodar o projeto local (DEBUG)

### 1. Instalações:

#### 1.2 Criar uma virtualenv para instalação das dependências

    virtualenv --python=$(which python3.8) env-meucontrole

#### 1.3 Ativação da virtualenv

    source env-meucontrole/bin/activate

#### 1.4 Instalação das dependências (Pasta raiz do projeto, e venv ativada (Passo 1.3))

    pip install -r requirements.txt

### 3. Executar servidor (com todas as dependências instaladas)

#### Cada servidor precisa de um terminal. Lembre-se de ativar a virtualenv ```source env-meucontrole/bin/activate```

#### 3 Executa o servidor do django

    ./manage.py runserver

