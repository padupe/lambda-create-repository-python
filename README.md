# lambda-create-repository-python

## Description
Creates a Repository on GitHub, using the service's API.
In addition, it adds the `"deploys"` and `"{Owner-Squad}-ADMIN"` teams of the Project Owner Squad and performs the dynamic creation of the `README.md`.

## Business Context
Team Tech <-> SRE <-> GitHub

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