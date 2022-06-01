# lambda-create-repository-python

## Description
Creates a Repository on GitHub, using the service's API.
In addition, it adds the `"deploys"` and `"{Owner-Squad}-ADMIN"` teams of the Project Owner Squad and performs the dynamic creation of the `README.md`.

## Flow
![img](https://github.com/padupe/lambda-create-repository-python/blob/main/docs/flow-lambda-create-repository.drawio.png)

## Business Context
Team Tech <-> SRE <-> GitHub

## Project Dependencies
- [mdutils](https://pypi.org/project/mdutils/ 'mdutils'): This Python package contains a set of basic tools that can help to create a markdown file while running a Python code;<br>
- [requests](https://pypi.org/project/requests/ 'requests'): Requests is a simple HTTP library;<br>

## Payload

### Payload Structure

<div align="center">

|Parameter|Value|Required|
|:---:|:---:|:---:|
|`repository_title`|`string`| `true`|
|`team_owner`|`string`|`true`|
|`private`|`boolean`|`true`|
|`about`|`string`|`true`|
|`description`|`string`|`true`|
|`business_context`|`string`|`true`|
|`requirements`|`array`|`true`|
|`integration`|`array`|`true`|

</div>

> NOTE: The "private" parameter can be passed as an empty string, as by default this property is "true".


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

## Status Code
- **201**
    - Repository Created
- **404**
    - Failure to find team `{team_owner}` at `{ORGANIZATION}`
    - Repository `{repository_title}` already exists at `{ORGANIZATION}`
- **500**
    - Error while running lambda: `{err}`

### Local Development

#### Requirements:
- CLI Serverless;
- Pip3;
- Python 3.8 =<.

#### Step by Step
1. Rename `serverless.yaml` to `serverles-prd.yaml`;

2. Rename `serverless-local.yaml` to `serverless.yaml`;

3. In the `configs` directory, in the `constants.py` file, enter a Personal Access Token (PAT) with Organization "Owner" privileges (permission to create repositories, link teams, etc.) in the `PAT_USER` constant;

4. In the `configs` directory, in the `constants.py` file, enter the name of the organization you belong to in the `ORGANIZATION` constant.

5. Run:
```
serverless invoke local --function create-repository --path example.json
```

**NOTE:**
A repository will be created with the name `**repository-test**` in your organization.