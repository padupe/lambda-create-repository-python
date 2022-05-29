from flask import Flask
import requests
import json
from mdutils.mdutils import MdUtils
import base64
from os import environ

GITURL = "https://api.github.com"
PAT_USER = ""
HEADER = {"Authorization": f"Bearer {PAT_USER}",
          "Content-Type": "application/vnd.github.v3+json"}
# ORGANIZATION = "madeiramadeirabr"
ORGANIZATION = "Pasto-1"
USER = "user"
DEPLOYS_TEAM = "deploys"


def run(event, context):
    repository_title = event["repository_title"]
    private = event["private"]
    team_owner = event["team_owner"]
    description = event["description"]
    business_context = event["business_context"]
    requirementes = event["requirements"]
    integration = event["integration"]
    
    if check_repository(repository_title).status_code == 404:
        if get_team_by_name(team_owner).status_code == 200:
            create_repository(repository_title, team_owner, private)
            add_team(repository_title, team_owner, permission_level='push')
            add_team(repository_title, f"{team_owner}-admin", permission_level='admin')
            add_team(repository_title, DEPLOYS_TEAM, permission_level='admin')
            
            if check_repository(repository_title).status_code == 200:
                create_readme(repository_title, description, business_context, team_owner, requirementes, integration)
                
                test_file = open("README.md", "rb")
                upload_readme_to_github(repository_title, test_file)
            
            return {
                "status": 201,
                "message": f'Repository {repository_title} created Successfully'            
                }
        
        else:
            return {
                "status": 404,
                "message": f'Failure to find team {team_owner} at {ORGANIZATION}.'
            }
    
    else:
        return {
            "status": 404,
            "message": f'Repository {repository_title} already exists at {ORGANIZATION}.'
        }


## GET team_id at Org
def get_team_by_id(team_name):
    find_team = requests.get(f'{GITURL}/orgs/{ORGANIZATION}/teams/{team_name}', headers=HEADER)
   
    team = json.loads(find_team.text)
    
    team_id = team["id"]
    
    return team_id


## GET team_name at Org
def get_team_by_name(team_name):
    team = requests.get(f'{GITURL}/orgs/{ORGANIZATION}/teams/{team_name}', headers=HEADER)
    return team

## Create Repository
def create_repository(repository_name, team_owner, private=None): 
    repository = format_string(repository_name)
    
    team_format = format_string(team_owner)
    team = get_team_by_id(team_format)
    
    if private == None:
        private = True
    
    payload = {
        "name": repository,
        "description": "Repository create with Lambda",
        "team_id": team,
        "private": private
    }
    
    data = json.dumps(payload)
    
    new_repository = requests.post(f'{GITURL}/orgs/{ORGANIZATION}/repos', headers=HEADER, data=data)
    
    if new_repository.status_code != 201:
        error_data = new_repository.text
        error_data = json.loads(error_data)
        
        return {
            "status": new_repository.status_code,
            "message": f"{error_data['message']}",
            "documentation_url": f"{error_data['documentation_url']}."          
        }
    
    return new_repository


## Verify respository_name already exists at Org
def check_repository(repository_name): 
    repository_format = format_string(repository_name)
    repository = requests.get(f'{GITURL}/repos/{ORGANIZATION}/{repository_format}', headers=HEADER)
    
    return repository


## Add Team an Repository
def add_team(repository_name, team_slug, permission_level=str):
    repository = format_string(repository_name)
    team = format_string(team_slug)
    
    payload = {
        "permission": permission_level
    }
    
    data = json.dumps(payload)
    
    result = requests.put(f'{GITURL}/orgs/{ORGANIZATION}/teams/{team}/repos/{ORGANIZATION}/{repository}', headers=HEADER, data=data)
    
    if result.status_code != 204:
        error_data = result.text
        error_data = json.loads(error_data)
        
        return {
            "status": result.status_code,
            "message": f"{error_data['message']}",
            "documentation_url": f"{error_data['documentation_url']}."          
        }
    
    return result


## Create README.md
def create_readme(title, description, bussiness_context, owner, requirements=list, integration=None):
    
    owner_link = format_string(owner)
    repository_title = format_string(title)
    
    markdow = MdUtils(file_name="README-test.md")
    
    markdow.new_header(level=1, title=repository_title)
    
    # Description
    markdow.new_header(level=2, title="Description")
    markdow.new_line(f'{description}\n')
    
    # Bussiness Context
    markdow.new_header(level=2, title="Bussiness Context")
    markdow.new_line(f'{bussiness_context}\n')
    
    # Requirements
    if requirements != None:
        markdow.new_header(level=2, title="Requirements")
        # markdow.new_list(items=[requirements], marked_with="-")
        for reqs in requirements:
            markdow.new_line(f'- {reqs}')
    
        markdow.new_line(f'')
        
    # Integration
    if integration != None:
        markdow.new_header(level=2, title="Integrations")
        
        for app_service in integration:
            markdow.new_line(f'- {app_service}')
            
        markdow.new_line(f'')
        
    # Owner
    markdow.new_header(level=2, title="Squad Owner")
    markdow.new_line(markdow.new_inline_link(link=f"https://github.com/orgs/{ORGANIZATION}/teams/{owner_link}", text=owner))
        
    readme_file = markdow.create_md_file()
    
    return readme_file

def format_string(parameter):
    lower_string = parameter.replace(" ", "-")
    result = lower_string.lower()
    
    return result

def encode_file_to_base64(file):
    data = file.read()
    encoded = base64.b64encode(data)
    print(f'FN "encode_file": {encoded}')
    return encoded

def upload_readme_to_github(repository, readme_file):
    readme = encode_file_to_base64(readme_file)
    
    path = readme_file if not 'README.md' else 'README.md'
    print(f'path: {path}')
    
    
    payload = {
        "message": "Upload README.md",
        "content": str(readme)
    }
    
    data = json.dumps(payload)
    
    print(f'payload after json.dumps(): {data}')
    
    result = requests.put(f'{GITURL}/repos/{ORGANIZATION}/{repository}/contents/{path}', headers=HEADER, data=data)
    
    print(f'RESULT =====> {result}')
    
    if result.status_code != 201:
        error_data = result.text
        error_data = json.loads(error_data)
        
        return {
            "status": result.status_code,
            "message": f"{error_data['message']}",
            "documentation_url": f"{error_data['documentation_url']}."          
        }
    
    return result
