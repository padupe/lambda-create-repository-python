# lambda-create-repository-python

## Description
Creates a Repository on GitHub, using the service's API.
In addition, it adds the `"deploys"` and `"{Owner-Squad}-ADMIN"` teams of the Project Owner Squad and performs the dynamic creation of the `README.md`.

## Business Context
Team Tech <-> SRE <-> GitHub

## Payload Example
```json
{
    "repository_title": "Repository-Test",
    "team_owner": "lambda-test",
    "private": true,
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

## Status Code
- **201**
    - Repository Created
- **404**
    - Failure to find team `{team_owner}` at `{ORGANIZATION}`
    - Repository `{repository_title}` already exists at `{ORGANIZATION}`
- **500**
    - Internal Error Server

### Local Development

Run Lambda:
```
serverless invoke local --function create-repository --path example.json
```