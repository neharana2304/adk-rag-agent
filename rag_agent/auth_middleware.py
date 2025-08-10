from typing import Callable

from auth0.management import Auth0
from rag_agent.config import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_CLIENT_SECRET,
    AUTH0_API_AUDIENCE,
)


class PermissionDeniedError(Exception):
    """Custom exception for permission denied errors."""

    pass

def get_auth0_client():
    return Auth0(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET
    )

def verify_agent_permissions(
    agent_name: str, required_permissions: list[str]
) -> bool:
    """Verifies agent permissions against Auth0."""
    auth0 = get_auth0_client()
    
    # In a real application, you would look up the user associated with the agent_name
    # For this example, we'll assume the agent_name corresponds to a user's email or username
    users = auth0.users.list(q=f'name:"{agent_name}"')
    
    if not users['users']:
        return False
        
    user_id = users['users'][0]['user_id']
    
    # Get the user's permissions
    permissions = auth0.users.get_permissions(user_id)
    
    user_permissions = {p['permission_name'] for p in permissions}
    
    return all(p in user_permissions for p in required_permissions)


def create_permission_wrapped_tool(
    tool_func: Callable, required_permissions: list[str], agent_name: str
) -> Callable:
    def wrapper(*args, **kwargs):
        if verify_agent_permissions(agent_name, required_permissions):
            return tool_func(*args, **kwargs)
        else:
            raise PermissionDeniedError(f"Agent '{agent_name}' lacks required permissions: {required_permissions}")

