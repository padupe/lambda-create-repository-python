from ast import Str
import string
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
ORGANIZATION = "madeiramadeirabr"
USER = "user"


def run(event, context):
    repository_title = event["repository_title"]
    private = event["private"]
    #team_owner = event["team"]
    
    if check_repository(repository_title).status_code == 404:
        create_repository(repository_title, private)
        
        return {
            "status": "200",
            "message": "Repository created Successfully"            
            }
    
    else:
        return {
            "status": "404",
            "message": "Repository already exists"
        }


def get_teams_by_name(team_name):
    team = requests.get(GITURL + "/orgs/" + ORGANIZATION + "/teams/" + team_name, headers=HEADER)
    
    return team


def create_repository(repository_name, private):
    
    payload = {
        "name": repository_name,
        "description": "Repository create with Lambda",
        "private": private
    }
    
    data = json.dumps(payload)
    
    new_repository = requests.post(f'{GITURL}/{USER}/repos', headers=HEADER, data=data)
    
    if new_repository.status_code == 404:
        return {
            "status": new_repository.status_code,
            "message": "Error at proccess 'create_repository'."            
        }
    
    return new_repository


def check_repository(repository_name):
    repository = requests.get(GITURL + "/repos/" + USER + "/" + repository_name, headers=HEADER)
    
    return repository


def create_readme(title, description, bussiness_context, requirements=list, integration=None, owner=None,):
    
    owner_link = owner.lower()
    
    markdow = MdUtils(file_name="README.md", title="README of Project.")
    
    markdow.new_header(level=1, title=title)
    
    # Description
    markdow.new_header(level=2, title="Description")
    markdow.new_paragraph(description)
    
    # Bussiness Context
    markdow.new_header(level=2, title="Bussiness Context")
    markdow.new_paragraph(bussiness_context)
    
    # Requirements
    markdow.new_header(level=2, title="Requirements")
    markdow.new_paragraph(requirements)
    
    # Integration
    if integration != None:
        markdow.new_header(level=2, title="Integrations")
        markdow.new_paragraph(integration)
        
    # Owner
    if owner != None:
        markdow.new_header(level=2, title="Squad Owner")
        markdow.new_line(markdow.new_inline_link(link=string("https://github.com/orgs/" + ORGANIZATION +"/teams/" + owner_link), text=owner))
        
    readme = markdow.create_md_file()
    
    return readme