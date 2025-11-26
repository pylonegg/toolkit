import requests
import logging
import json

# ---------------------------
# Helper functions
# ---------------------------

def _prepare_headers(token: str):
    """Return standard headers for SCIM API calls."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


def _normalize_host(host: str):
    """Remove trailing slash from host URL."""
    return host.rstrip("/")


def get_user(databricks_host: str, token: str, email: str):
    """Retrieve a user by email. Returns user dict or None if not found."""
    databricks_host = _normalize_host(databricks_host)
    headers = _prepare_headers(token)

    search_url = f"{databricks_host}/api/2.0/preview/scim/v2/Users?filter=userName%20eq%20%22{email}%22"
    res = requests.get(search_url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"User search failed: {res.status_code} {res.text}")

    users = res.json().get("Resources", [])
    return users[0] if users else None


def get_group(databricks_host: str, token: str, group_name: str):
    """Retrieve a group by displayName. Returns group dict or None if not found."""
    databricks_host = _normalize_host(databricks_host)
    headers = _prepare_headers(token)

    group_search_url = f"{databricks_host}/api/2.0/preview/scim/v2/Groups?filter=displayName%20eq%20%22{group_name}%22"
    res = requests.get(group_search_url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Group search failed: {res.status_code} {res.text}")

    groups = res.json().get("Resources", [])
    return groups[0] if groups else None


# ---------------------------
# Main functions
# ---------------------------
# --- User -----------------------------------------------------
# Function relating to Users in Databricks Unity Catalog.

# --- User Add -----------------------------------------------------
def create_user(databricks_host: str, token: str, email: str, display_name: str | None = None):
    """
    Add a user to Databricks Unity Catalog using SCIM REST API.
    Returns the user dict.
    """
    logging.info(f"Adding user {email} to Unity Catalog.")

    existing_user = get_user(databricks_host, token, email)
    if existing_user:
        logging.info(f"User already exists: {existing_user['id']}")
        return existing_user

    databricks_host = _normalize_host(databricks_host)
    headers = _prepare_headers(token)

    payload = {
        "userName": email,
        "displayName": display_name or email.split("@")[0],
        "active": True
    }

    create_url = f"{databricks_host}/api/2.0/preview/scim/v2/Users"
    res = requests.post(create_url, headers=headers, json=payload)
    if res.status_code not in (200, 201):
        raise Exception(f"User creation failed: {res.status_code} {res.text}")

    user = res.json()
    logging.info(f"Created user: {user['id']}")
    return user


# --- Show User Details -----------------------------------------------------
def show_user(databricks_host: str, token: str, email: str) -> dict:
    """
    Retrieve full user details from Databricks Unity Catalog (SCIM API).
    
    Returns the user dictionary containing:
      - id
      - userName (email)
      - displayName
      - active status
      - groups (if included)
      - etc.
    
    Raises Exception if user not found.
    """
    databricks_host = _normalize_host(databricks_host)
    headers = _prepare_headers(token)

    url = f"{databricks_host}/api/2.0/preview/scim/v2/Users?filter=userName eq \"{email}\""
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch user details: {res.status_code} {res.text}")

    users = res.json().get("Resources", [])
    if not users:
        raise Exception(f"User not found: {email}")

    user = users[0]
    pretty = json.dumps(user, indent=2)

    logging.info(f"Retrieved details for user {email}: ID={user['id']}")
    logging.info(f"Details: \n {pretty}")
    return user





# --- Group -----------------------------------------------------
# Function relating to groups in Databricks Unity Catalog.

# --- Group Add User -----------------------------------------------------
def group_add_user(databricks_host: str, token: str, user_email: str, group_name: str):
    """
    Add a Databricks user to a Unity Catalog group using SCIM REST API.
    Returns dict with user_id and group_id.
    """
    user = get_user(databricks_host, token, user_email)
    if not user:
        raise Exception(f"User not found: {user_email}")
    user_id = user["id"]
    logging.info(f"Found user {user_email}: ID={user_id}")

    group = get_group(databricks_host, token, group_name)
    if not group:
        raise Exception(f"Group not found: {group_name}")
    group_id = group["id"]
    logging.info(f"Found group {group_name}: ID={group_id}")

    databricks_host = _normalize_host(databricks_host)
    headers = _prepare_headers(token)

    patch_url = f"{databricks_host}/api/2.0/account/scim/v2/Groups/{group_id}"
    
    patch_payload = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        "Operations": [
            {
                "op": "add",
                "path": "members",
                "value": [{"value": user_id}]
            }
        ]
    }

    res = requests.patch(patch_url, headers=headers, json=patch_payload)
    if res.status_code not in (200, 204):
        raise Exception(f"Failed to add user to group: {res.status_code} {res.text}")

    logging.info(f"Added user {user_email} to group {group_name}")
    return {"user_id": user_id, "group_id": group_id}



# --- External Locations  ---------------------------

def create_external_location(
        databricks_host: str,
        token: str,
        storage_account: str,
        container: str,
        comment: str | None = None,
        force: bool = False
    ):
    """
    Create a Unity Catalog External Location.

    Args:
        databricks_host: Databricks workspace URL (https://...).
        token: Personal Access Token.
        name: Name of the external location.
        url: Full path to the storage location (e.g., abfss://container@account.dfs.core.windows.net/path).
        credential_name: Name of the Storage Credential to associate.
        comment: Optional comment string.
        force: If True, allows update of an existing external location.

    Returns:
        The created External Location as a dict.
    """
    logging.info(f"Creating external location: {container}")

    url = f"abfss://{container}@{storage_account}.dfs.core.windows.net/"
    credential_name = f"{storage_account}"
    name = container

    databricks_host = _normalize_host(databricks_host)
    headers = _prepare_headers(token)

    payload = {
        "name": name,
        "url": url,
        "credential_name": credential_name,
        "comment": comment or "",
        "force": force
    }

    url_api = f"{databricks_host}/api/2.1/unity-catalog/external-locations"

    res = requests.post(url_api, headers=headers, json=payload)

    if res.status_code not in (200, 201):
        raise Exception(
            f"External Location creation failed: {res.status_code} {res.text}"
        )

    details = res.json()
    logging.info(f"External Location created: {name} (ID={details.get('name')})")
    return details
