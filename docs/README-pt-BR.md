![img](https://github.com/padupe/lambda-create-repository-python/blob/main/assets/banner_project.png)
# lambda-create-repository-python

<div align="center">

[![Technology][python-image]][python-url]
[![Technology][aws-lambda-image]][aws-lambda-url]<br>

![img](https://img.shields.io/badge/python-v3.8-blue)
![img](https://img.shields.io/badge/mdutils-v1.3.1-blue)
![img](https://img.shields.io/badge/requests-v2.25.1-blue)

</div>

[python-url]: https://www.python.org/
[python-image]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

[aws-lambda-url]: https://aws.amazon.com/pt/lambda/
[aws-lambda-image]: https://img.shields.io/badge/aws.lambda-yellow?style=for-the-badge&logo=amazon&logoColor=black

## Índice
<!--ts-->
* [lambda-create-repository-python](#lambda-create-repository-python)
    * [Índice](#indice)
    * [Descrição](#descricao)
    * [Fluxo](#fluxo)
    * [Contexto de Negócio](#contexto-de-negocio)
    * [Dependências do Projeto](#dependencias-do-projeto)
    * [Payload](#payload)
        * [Estrutura do Payload](#estrutura-do-payload)
        * [Payload de Exemplo (Completo)](#payload-de-exemplo-completo)
        * [Payload de Exemplo (Simples)](#payload-de-exemplo-simples)
    * [Status Code](#status-code)
    * [Desenvolvimento Local](#desenvolvimento-local)
        * [Requisitos](#requisitos)
        * [Passo a Passo](#passo-a-passo)
<!--te-->

## Descrição
Cria um Repositório no GitHub, usando a API do serviço.
Além disso, adiciona as equipes `"deploys"` e `"{Owner-Squad}-ADMIN"` da Squad "Dona" do Projeto e realiza a criação dinâmica do `README.md`.

## Fluxo
![img](https://github.com/padupe/lambda-create-repository-python/blob/main/docs/flow-lambda-create-repository.drawio.png)

## Contexto de Negócio
Permitir um gerenciamento dinâmico no processo de criação de repositórios da organização.<br>

Time Tech <-> **Time responsável pelo gerenciamento do GitHub na Organização** <-> GitHub

## Dependências do Projeto
- [mdutils](https://pypi.org/project/mdutils/ 'mdutils'): Este pacote Python contém um conjunto de ferramentas básicas que podem ajudar a criar um arquivo markdown ao executar um código Python;<br>
- [requests](https://pypi.org/project/requests/ 'requests'): Requests é uma biblioteca HTTP simples.<br>

## Payload

## Estrutura do Payload

<div align="center">

|Parâmetro|Valor|Requirido|
|:---:|:---:|:---:|
|`repository_title`|`string`|`verdadeiro`|
|`team_owner`|`string`|`verdadeiro`|
|`private`|`boolean`|`verdadeiro`|
|`about`|`string`|`verdadeiro`|
|`description`|`string`|`verdadeiro`|
|`business_context`|`string`|`verdadeiro`|
|`requirements`|`array`|`verdadeiro`|
|`integration`|`array`|`verdadeiro`|

</div>

### Payload de Exemplo (Completo)
```json
{
    "repository_title": "Repository-Test",
    "team_owner": "lambda-test",
    "private": true,
    "about": "Repository create with Lambda",
    "description": "An repository test.",
    "business_context": "Repository test with Lambda",
    "requirements": [
        "Nodejs",
        "Docker"
    ],
    "integration": [
        "Life-Cycle",
        "Order-Service"
    ]
}
```
> NOTA: O parâmetro "private" pode ser passado como uma string vazia, pois por padrão esta propriedade é "true".

### Payload de Exemplo (Simples)
```json
{
    "repository_title": "Repository-Test-Two",
    "team_owner": "lambda-test",
    "private": "",
    "about": "Repository create with Lambda",
    "description": "An repository test.",
    "business_context": "Repository test with Lambda",
    "requirements": [],
    "integration": []
}
```
> NOTA: O parâmetro "private" pode ser passado como uma string vazia, pois por padrão esta propriedade é "true".

## Status Code
- **201**
    - Repository Created<br>
    *(Repositório Criado)*
- **404**
    - Failure to find team `{team_owner}` at `{ORGANIZATION}`<br>
    *(Falha ao encontrar a equipe `{team_owner}` em `{ORGANIZATION}`)*
    - Repository `{repository_title}` already exists at `{ORGANIZATION}`<br>
    *O repositório `{repository_title}` já existe em `{ORGANIZATION}`*
- **500**
    - Error while running lambda: `{err}`<br>
    *Erro ao executar lambda: `{err}`*

## Desenvolvimento Local

### Requisitos
- CLI [Serverless](https://www.serverless.com/framework/docs/getting-started);
- Pip3;
- Python 3.8 =<.

### Passo a Passo
1. Renomeie `serverless.yaml` para `serverles-prd.yaml`;

2. Renomeie `serverless-local.yaml` para `serverless.yaml`;

3. No diretório `configs`, no arquivo [`constants.py`](https://github.com/padupe/lambda-create-repository-python/blob/main/configs/constants.py), insira um *Personal Access Token (PAT)* (Token de Acesso Pessoal) com privilégios de "Proprietário" da Organização (permissão para criar repositórios, vincular equipes, etc.) na constante `PAT_USER`;

4. No diretório `configs`, no arquivo [`constants.py`](https://github.com/padupe/lambda-create-repository-python/blob/main/configs/constants.py), digite o nome da organização à qual você pertence na constante `ORGANIZATION`;

    4.1. Se a sua organização não possuir times auxiliares (`"{Owner-Squad}-ADMIN"`, `"deploys"`, etc), comente (ou remova) as linhas 21 e 22 do arquivo [`app.py`](https://github.com/padupe/lambda-create-repository-python/blob/main/app/app.py).

5. Rode o comando:
```
serverless invoke local --function create-repository --path example.json
```

**NOTA:**
Um repositório será criado com o nome **`repository-test`** em sua organização.