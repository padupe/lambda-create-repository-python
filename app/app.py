from asyncio import events
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
        event_arg = event
        
        print(f'Event Args: {event_arg}')
        print(f'Repository in Arg: {"repository_title" in event_arg}')
        print(f'Private in Arg: {"private" in event_arg}')
        print(f'About in Arg: {"about" in event_arg}')
        print(f'Team Owner in Arg: {"team_owner" in event_arg}')
        print(f'Description in Arg: {"description" in event_arg}')
        print(f'Business Context in Arg: {"business_context" in event_arg}')
        print(f'Requirements in Arg: {"requirements" in event_arg}')
        print(f'Integration in Arg: {"integration" in event_arg}')
        
        # if "repository_title" in event_arg and repository_title != "" and "private" in event_arg and private != "" and "about" in event_arg and about != "" and "team_owner" in event_arg and team_owner != "" and "description" in event_arg and description != "" and "business_context" in event_arg and business_context != "" and "requirementes" in event_arg and requirementes != "" and "integration" in event_arg and integration != "":
        if "repository_title" in event_arg and "private" in event_arg and "about" in event_arg and "team_owner" in event_arg and "description" in event_arg and "business_context" in event_arg and "requirementes" in event_arg and "integration" in event_arg:
            print("Todos parâmetros foram informados")
            if GitHubService.check_repository(self=None, repository_name=repository_title).status_code == 404:
                print("Criando Repo.")
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
        else:
            print("ERROOOO")
    except Exception as err:
        return {
            "status": 500,
            "message": f'Error while running lambda: {err}.'
        }