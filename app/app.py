from configs import constants
from services.github_service import GitHubService
from services.mdutils_service import MdUtilsService
from helpers import remove_tmp_file as RemoveTMP

def run(event, context):
    try:
        repository_title = event["repository_title"]
        private = event["private"]
        about = event["about"]
        team_owner = event["team_owner"]
        description = event["description"]
        business_context = event["business_context"]
        requirementes = event["requirements"]
        integration = event["integration"]
        
        if GitHubService.check_repository(self=None, repository_name=repository_title).status_code == 404:
            if GitHubService.get_team_by_name(self=None, team_name=team_owner).status_code == 200:
                GitHubService.create_repository(self=None, repository_name=repository_title, team_owner=team_owner, about=about, private=private)
                GitHubService.add_team(self=None, repository_name=repository_title, team_slug=team_owner, permission_level='push')
                GitHubService.add_team(self=None, repository_name=repository_title, team_slug=f"{team_owner}-admin", permission_level='admin')
                GitHubService.add_team(self=None, repository_name=repository_title, team_slug=constants.DEPLOYS_TEAM, permission_level='admin')
                
                if GitHubService.check_repository(self=None, repository_name=repository_title).status_code == 200:
                    readme_file = MdUtilsService.create_readme(self=None, title=repository_title, description=description, bussiness_context=business_context, owner=team_owner, requirements=requirementes, integration=integration)
                    GitHubService.upload_readme_to_github(self=None, repository_name=repository_title, readme_file=readme_file)
                    RemoveTMP.remove_tmp_file(readme_file)
                
                return {
                    "status": 201,
                    "message": f'Repository {repository_title} created Successfully'            
                    }
            
            else:
                return {
                    "status": 404,
                    "message": f'Failure to find team {team_owner} at {constants.ORGANIZATION}.'
                }
        
        else:
            return {
                "status": 404,
                "message": f'Repository {repository_title} already exists at {constants.ORGANIZATION}.'
            }
    except Exception as err:
        return {
            "status": 500,
            "message": f'Error while running lambda: {err}.'
        }