USER_ROLES = {
    "admin": ["vectorstore", "database", "web"],
    "employee": ["vectorstore", "web"],
    "guest": ["web"]
}

def is_authorized(user_role: str, target: str) -> bool:
    return target in USER_ROLES.get(user_role.lower(), [])
