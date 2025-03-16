from fastapi import HTTPException
from oso import Oso

oso = Oso()

def initialize_oso():
    """Initialize Oso and load the policy file."""
    try:
        oso.load_file("app/rbac/policies.polar")  # Load the Oso policy file
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load Oso policies: {str(e)}")

def authorize(actor, action, resource):
    """Authorize a user action on a resource using Oso."""
    if not oso.is_allowed(actor, action, resource):
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")