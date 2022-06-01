from os import environ

GITHUB_URL = "https://api.github.com"
PAT_USER = "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"
HEADER = {"Authorization": f"Bearer {PAT_USER}",
          "Content-Type": "application/vnd.github.v3+json"}
# ORGANIZATION = "madeiramadeirabr"
ORGANIZATION = "Pasto-1"
USER = "user"
DEPLOYS_TEAM = "deploys"

"""

TODO - Create Secrets Manager on AWS:

PAT_USER = environ["PAT_USER"]
"""