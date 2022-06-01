import requests
import json
from configs import constants
from helpers import format_string as Format
from helpers import encode_file_to_base64 as EncodeFile

class GitHubService:
    
    def __init__(self, repository_name, team_name, team_slug, about, private, readme_file, permission_level):
        self.repository_name = repository_name
        self.team_name = team_name
        self.team_slug = team_slug
        self.about = about
        self.private = private
        self.readme_file = readme_file
        self.permission_level = permission_level
        
    ## GET team_id at Org
    def get_team_by_id(self, team_name):
        find_team = requests.get(f'{constants.GITHUB_URL}/orgs/{constants.ORGANIZATION}/teams/{team_name}', headers=constants.HEADER)
        team = json.loads(find_team.text) 
        team_id = team["id"]
        return team_id

    ## GET team_name at Org
    def get_team_by_name(self, team_name):
        team = requests.get(f'{constants.GITHUB_URL}/orgs/{constants.ORGANIZATION}/teams/{team_name}', headers=constants.HEADER)
        return team

    ## Create Repository
    def create_repository(self, repository_name, team_owner, about, private=None):
        repository = Format.format_string(repository_name)
        team_format = Format.format_string(team_owner)
        team = GitHubService.get_team_by_id(self, team_format)
        
        if private == None:
            private = True
        
        payload = {
            "name": repository,
            "description": about,
            "team_id": team,
            "private": private
        }
        
        data = json.dumps(payload)
        
        new_repository = requests.post(f'{constants.GITHUB_URL}/orgs/{constants.ORGANIZATION}/repos', headers=constants.HEADER, data=data)
        
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
    def check_repository(self, repository_name): 
        repository_format = Format.format_string(repository_name)
        repository = requests.get(f'{constants.GITHUB_URL}/repos/{constants.ORGANIZATION}/{repository_format}', headers=constants.HEADER)
        return repository


    ## Add Team an Repository
    def add_team(self, repository_name, team_slug, permission_level=str):
        repository = Format.format_string(repository_name)
        team = Format.format_string(team_slug)
        
        payload = {
            "permission": permission_level
        }
        
        data = json.dumps(payload)
        
        result = requests.put(f'{constants.GITHUB_URL}/orgs/{constants.ORGANIZATION}/teams/{team}/repos/{constants.ORGANIZATION}/{repository}', headers=constants.HEADER, data=data)
        
        if result.status_code != 204:
            error_data = result.text
            error_data = json.loads(error_data)
            
            return {
                "status": result.status_code,
                "message": f"{error_data['message']}",
                "documentation_url": f"{error_data['documentation_url']}."          
            }
        
        return result

    def upload_readme_to_github(self, repository_name, readme_file):
        readme = EncodeFile.encode_file_to_base64(readme_file)
        path = readme_file if not 'README.md' else 'README.md'
            
        payload = {
            "message": "Upload README.md",
            # REVER -> se é preciso passar str
            "content": str(readme)
        }
        
        data = json.dumps(payload)
        
        result = requests.put(f'{constants.GITHUB_URL}/repos/{constants.ORGANIZATION}/{repository_name}/contents/{path}', headers=constants.HEADER, data=data)
        
        if result.status_code != 201:
            error_data = result.text
            error_data = json.loads(error_data)
            
            return {
                "status": result.status_code,
                "message": f"{error_data['message']}",
                "documentation_url": f"{error_data['documentation_url']}."        
            }
        
        return result