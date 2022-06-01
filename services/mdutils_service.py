from mdutils.mdutils import MdUtils
from helpers import format_string as FormatSTR
from configs import constants

class MdUtilsService:
    def __init__(self, title, description, bussiness_context, owner, requirements=None, integration=None):
        self.title = title
        self.description = description
        self.bussiness_context = bussiness_context
        self.owner = owner
        self.requirements = requirements
        self.integration = integration  
    
    ## Create README.md
    def create_readme(self, title, description, bussiness_context, owner, requirements=None, integration=None):
        
        owner_link = FormatSTR.format_string(owner)
        repository_title = FormatSTR.format_string(title)
        
        markdown = MdUtils(file_name="README-created.md")
        
        # Title
        markdown.new_header(level=1, title=repository_title)
        
        # Description
        markdown.new_header(level=2, title="Description")
        markdown.new_line(f'{description}\n')
        
        # Bussiness Context
        markdown.new_header(level=2, title="Bussiness Context")
        markdown.new_line(f'{bussiness_context}\n')
        
        # Owner
        markdown.new_header(level=2, title="Squad Owner")
        markdown.new_line(markdown.new_inline_link(link=f"https://github.com/orgs/{constants.ORGANIZATION}/teams/{owner_link}", text=owner))
        
        # Requirements
        if len(requirements) != 0:
            markdown.new_header(level=2, title="Requirements")
            # markdown.new_list(items=[requirements], marked_with="-")
            for reqs in requirements:
                markdown.new_line(f'- {reqs}')
        
            markdown.new_line(f'')
            
        # Integration
        if len(integration) != 0:
            markdown.new_header(level=2, title="Integrations")
            
            for app_service in integration:
                markdown.new_line(f'- {app_service}')
                
            markdown.new_line(f'')  
            
        readme_file = markdown.create_md_file()
        
        readme = open("README-created.md", "rb")
        
        return readme