from os import environ

GITHUB_URL = "https://api.github.com"
PAT_USER = ""
HEADER = {"Authorization": f"Bearer {PAT_USER}",
          "Content-Type": "application/vnd.github.v3+json"}
ORGANIZATION = "Pasto-1"
DEPLOYS_TEAM = "deploys"

"""
TODO - Create Secrets Manager on AWS:

PAT_USER = environ["PAT_USER"]
"""