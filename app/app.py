from flask import Flask
import requests
import json
from mdutils.mdutils import MdUtils
import base64
import os

GITURL = "https://api.github.com"
PAT_USER = "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"
HEADER = {"Authorization": f"Bearer {PAT_USER}",
          "Content-Type": "application/vnd.github.v3+json"}
# ORGANIZATION = "madeiramadeirabr"
ORGANIZATION = "Pasto-1"
USER = "user"
DEPLOYS_TEAM = "deploys"


def run(event, context):
    repository_title = event["repository_title"]
    private = event["private"]
    about = event["about"]
    team_owner = event["team_owner"]
    description = event["description"]
    business_context = event["business_context"]
    requirementes = event["requirements"]
    integration = event["integration"]
    
    if check_repository(repository_title).status_code == 404:
        if get_team_by_name(team_owner).status_code == 200:
            create_repository(repository_title, team_owner, about, private)
            add_team(repository_title, team_owner, permission_level='push')
            add_team(repository_title, f"{team_owner}-admin", permission_level='admin')
            add_team(repository_title, DEPLOYS_TEAM, permission_level='admin')
            
            if check_repository(repository_title).status_code == 200:
                readme_file = create_readme(repository_title, description, business_context, team_owner, requirementes, integration)
                upload_readme_to_github(repository_title, readme_file)
                remove_tmp_file(readme_file)
            
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
def create_repository(repository_name, team_owner, about, private=None): 
    repository = format_string(repository_name)
    
    team_format = format_string(team_owner)
    team = get_team_by_id(team_format)
    
    if private == None:
        private = True
    
    payload = {
        "name": repository,
        "description": about,
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
    
    markdown = MdUtils(file_name="README-created.md")
    
    markdown.new_header(level=1, title=repository_title)
    
    # Description
    markdown.new_header(level=2, title="Description")
    markdown.new_line(f'{description}\n')
    
    # Bussiness Context
    markdown.new_header(level=2, title="Bussiness Context")
    markdown.new_line(f'{bussiness_context}\n')
    
    # Requirements
    if requirements != None:
        markdown.new_header(level=2, title="Requirements")
        # markdown.new_list(items=[requirements], marked_with="-")
        for reqs in requirements:
            markdown.new_line(f'- {reqs}')
    
        markdown.new_line(f'')
        
    # Integration
    if integration != None:
        markdown.new_header(level=2, title="Integrations")
        
        for app_service in integration:
            markdown.new_line(f'- {app_service}')
            
        markdown.new_line(f'')
        
    # Owner
    markdown.new_header(level=2, title="Squad Owner")
    markdown.new_line(markdown.new_inline_link(link=f"https://github.com/orgs/{ORGANIZATION}/teams/{owner_link}", text=owner))
        
    readme_file = markdown.create_md_file()
    
    readme = open("README-created.md", "rb")
    
    return readme

def format_string(parameter):
    lower_string = parameter.replace(" ", "-")
    result = lower_string.lower()
    
    return result

def encode_file_to_base64(file):
    data = file.read()
    file_base64 = str(base64.b64encode(data))
    encoded = file_base64.split("'")[1]
    return encoded

def upload_readme_to_github(repository, readme_file):
    readme = encode_file_to_base64(readme_file)
    path = readme_file if not 'README.md' else 'README.md'
        
    payload = {
        "message": "Upload README.md",
        # REVER -> se é preciso passar str
        "content": str(readme)
    }
    
    data = json.dumps(payload)
    
    result = requests.put(f'{GITURL}/repos/{ORGANIZATION}/{repository}/contents/{path}', headers=HEADER, data=data)
    
    if result.status_code != 201:
        error_data = result.text
        error_data = json.loads(error_data)
        
        return {
            "status": result.status_code,
            "message": f"{error_data['message']}",
            "documentation_url": f"{error_data['documentation_url']}."        
        }
    
    return result

def remove_tmp_file(file):
    
    if os.path.exists(file.name):
        os.remove(file.name)
    else:
        return {
            "status": 500,
            "message": f'Error deleting file {file.name}.'
        }