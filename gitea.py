import aiohttp
from typing import Dict, Any, List
from config import GITEA_TOKEN, GITEA_URL, GITEA_USERNAME


async def request(method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """ Make a request to the Gitea API. """
    url = f"{GITEA_URL}/api/v1/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"token {GITEA_TOKEN}",
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
        
async def get_user(username: str) -> Dict[str, Any]:
    """ Get a user from Gitea. """
    return await request("GET", f"/users/{username}")

async def list_repos(username: str) -> Dict[str, Any]:
    """ List repositories for a user. """
    return await request("GET", f"/users/{username}/repos")

# async def list_templates() -> Dict[str, Any]:
#     """ List templates. """
#     return await request("GET", "/templates")

async def create_repo(name: str, description: str, private: bool = False) -> Dict[str, Any]:
    """ Create a new repository. """
    data = {
        "name": name,
        "description": description,
        "private": private,
    }
    return await request("POST", "/user/repos", json=data)

async def create_repo_from_template(template_owner: str,template_repo: str,new_owner: str,new_repo: str,description: str = "",private: bool = False) -> Dict[str, Any]:
    """ Create a new repository from a template. """
    data = {
        "owner": new_owner,
        "name": new_repo,
        "description": description,
        "private": private
    }
    return await request(
        "POST", 
        f"/repos/{template_owner}/{template_repo}/generate",
        json=data
    )