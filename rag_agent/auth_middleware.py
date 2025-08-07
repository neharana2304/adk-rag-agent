from typing import Callable


class PermissionDeniedError(Exception):
    """Custom exception for permission denied errors."""

    pass


def verify_agent_permissions(
    agent_name: str, required_permissions: list[str]
) -> bool:
    """Placeholder function to verify agent permissions."""
    if agent_name == "RagAgent" and "rag:read" in required_permissions:
        return True
    if agent_name == "RagAgent" and "rag:write" in required_permissions:
        return True
    return False


def create_permission_wrapped_tool(
    tool_func: Callable, required_permissions: list[str], agent_name: str
) -> Callable:
    def wrapper(*args, **kwargs):
        if not verify_agent_permissions(agent_name, required_permissions):
            raise PermissionDeniedError("Permission denied")
        return tool_func(*args, **kwargs)
