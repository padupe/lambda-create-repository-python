![img](https://github.com/padupe/lambda-create-repository-python/blob/main/assets/banner_project.png)
<div align="center">

![GitHub Repo stars](https://img.shields.io/github/stars/padupe/lambda-create-repository-python?color=blue&label=stars)
![GitHub forks](https://img.shields.io/github/forks/padupe/lambda-create-repository-python?color=blue&label=forks)
![GitHub last commit](https://img.shields.io/github/last-commit/padupe/lambda-create-repository-python?color=blue&label=last%20commit)

</div>

# lambda-create-repository-python
> Check the Documentation in pt-BR by clicking 🇧🇷 [here](https://github.com/padupe/lambda-create-repository-python/blob/main/docs/README-pt-BR.md 'here').

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

## Index
<!--ts-->
* [lambda-create-repository-python](#lambda-create-repository-python)
    * [Index](#index)
    * [Description](#description)
    * [Flow](#flow)
    * [Business Context](#bussiness-context)
    * [Project Dependencies](#project-dependencies)
    * [Payload](#payload)
        * [Payload Structure](#payload-structure)
        * [Payload Example (Complete)](#payload-example-complete)
        * [Payload Example (Simple)](#payload-example-simple)
    * [Status Code](#status-code)
    * [Local Development](#local-development)
        * [Requirements](#requirements)
        * [Step by Step](#step-by-step)
<!--te-->

## Description
Creates a Repository on GitHub, using the service's API.
In addition, it adds the `"deploys"` and `"{Owner-Squad}-ADMIN"` teams of the Project Owner Squad and performs the dynamic creation of the `README.md`.

## Flow
![img](https://github.com/padupe/lambda-create-repository-python/blob/main/docs/flow-lambda-create-repository.drawio.png)

## Bussiness Context
Allow a dynamic management in the organization's repository creation process.<br>

Team Tech <-> **Team responsible for managing GitHub in the Organization** <-> GitHub

## Project Dependencies
- [mdutils](https://pypi.org/project/mdutils/ 'mdutils'): This Python package contains a set of basic tools that can help to create a markdown file while running a Python code;<br>
- [requests](https://pypi.org/project/requests/ 'requests'): Requests is a simple HTTP library.<br>

## Payload

### Payload Structure

<div align="center">

|Parameter|Value|Required|
|:---:|:---:|:---:|
|`repository_title`|`string`|`true`|
|`team_owner`|`string`|`true`|
|`private`|`boolean`|`true`|
|`about`|`string`|`true`|
|`description`|`string`|`true`|
|`business_context`|`string`|`true`|
|`requirements`|`array`|`true`|
|`integration`|`array`|`true`|

</div>

### Payload Example (Complete)
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
> NOTE: The "private" parameter can be passed as an empty string, as by default this property is "true".

### Payload Example (Simple)
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
> NOTE: The "private" parameter can be passed as an empty string, as by default this property is "true".

## Status Code
- **201**
    - Repository Created
- **404**
    - Failure to find team `{team_owner}` at `{ORGANIZATION}`
    - Repository `{repository_title}` already exists at `{ORGANIZATION}`
- **500**
    - Error while running lambda: `{err}`

## Local Development

### Requirements:
- CLI [Serverless](https://www.serverless.com/framework/docs/getting-started);
- Pip3;
- Python 3.8 =<.

### Step by Step
1. Rename `serverless.yaml` to `serverles-prd.yaml`;

2. Rename `serverless-local.yaml` to `serverless.yaml`;

3. In the `configs` directory, in the [`constants.py`](https://github.com/padupe/lambda-create-repository-python/blob/main/configs/constants.py) file, enter a Personal Access Token (PAT) with Organization "Owner" privileges (permission to create repositories, link teams, etc.) in the `PAT_USER` constant;

4. In the `configs` directory, in the [`constants.py`](https://github.com/padupe/lambda-create-repository-python/blob/main/configs/constants.py) file, enter the name of the organization you belong to in the `ORGANIZATION` constant;

5. Run:
```
serverless invoke local --function create-repository --path example.json
```

**NOTE:**
A repository will be created with the name **`repository-test`** in your organization.
