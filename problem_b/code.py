"""
Helpers for user display and lookup. Used by the dashboard.
"""

def get_user_display(user_id):
    import requests
    r = requests.get("https://api.example.com/users/" + str(user_id))
    data = r.json()
    return data["name"], data["email"]


def get_user_list(role=None):
    """Fetch users, optionally filter by role. Returns list of dicts."""
    import requests
    url = "https://api.example.com/users"
    if role:
        url += "?role=" + role
    r = requests.get(url)
    users = r.json()
    result = []
    for u in users:
        result.append({
            "id": u["id"],
            "name": u["name"],
            "email": u["email"],
            "role": u.get("role", "user"),
        })
    return result


def format_user_for_header(user_id):
    """Return a short string for dashboard header: 'Name' or 'Name (role)'."""
    name, email = get_user_display(user_id)
    user_list = get_user_list()
    for u in user_list:
        if u["id"] == user_id:
            return f"{name} ({u['role']})"
    return name


def lookup_by_email(email):
    """Find user id for a given email. Used by support tool."""
    users = get_user_list()
    for u in users:
        if u["email"] == email:
            return u["id"]
    return None
