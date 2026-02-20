import requests

# Configuration
GITLAB_URL = "https://gitlab.com"  # Change for self-hosted: https://gitlab.example.com
PRIVATE_TOKEN = "your_personal_access_token"
PROJECT_ID = "your_project_id"  # Can be numeric ID or "namespace/project-name"

headers = {
    "PRIVATE-TOKEN": PRIVATE_TOKEN,
    "Content-Type": "application/json"
}

base_url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/variables"


# ── List all variables ────────────────────────────────────────────────────────
def list_variables():
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()
    variables = response.json()
    for var in variables:
        print(f"Key: {var['key']}, Value: {var['value']}, Protected: {var['protected']}, Masked: {var['masked']}")
    return variables


# ── Get a specific variable ───────────────────────────────────────────────────
def get_variable(key, environment_scope=None):
    url = f"{base_url}/{key}"
    params = {}
    if environment_scope:
        params["filter[environment_scope]"] = environment_scope
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    var = response.json()
    print(f"Key: {var['key']}, Value: {var['value']}")
    return var


# ── Create a variable ─────────────────────────────────────────────────────────
def create_variable(key, value, protected=False, masked=False, variable_type="env_var", environment_scope="*"):
    payload = {
        "key": key,
        "value": value,
        "variable_type": variable_type,  # "env_var" or "file"
        "protected": protected,
        "masked": masked,
        "environment_scope": environment_scope
    }
    response = requests.post(base_url, headers=headers, json=payload)
    response.raise_for_status()
    print(f"Created variable: {response.json()['key']}")
    return response.json()


# ── Update a variable ─────────────────────────────────────────────────────────
def update_variable(key, value, protected=False, masked=False, environment_scope="*"):
    url = f"{base_url}/{key}"
    payload = {
        "value": value,
        "protected": protected,
        "masked": masked,
        "environment_scope": environment_scope
    }
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    print(f"Updated variable: {response.json()['key']}")
    return response.json()


# ── Delete a variable ─────────────────────────────────────────────────────────
def delete_variable(key):
    url = f"{base_url}/{key}"
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    print(f"Deleted variable: {key}")


# ── Upsert (create or update) ─────────────────────────────────────────────────
def upsert_variable(key, value, protected=False, masked=False, environment_scope="*"):
    try:
        get_variable(key)
        return update_variable(key, value, protected, masked, environment_scope)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return create_variable(key, value, protected, masked, environment_scope=environment_scope)
        raise


# ── Example usage ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # List all variables
    print("=== All Variables ===")
    list_variables()

    # Get a specific variable
    print("\n=== Get Variable ===")
    get_variable("MY_VAR")

    # Create a new variable
    print("\n=== Create Variable ===")
    create_variable("NEW_VAR", "hello_world", protected=False, masked=False)

    # Update an existing variable
    print("\n=== Update Variable ===")
    update_variable("MY_VAR", "updated_value", protected=True, masked=True)

    # Upsert (create if not exists, update if exists)
    print("\n=== Upsert Variable ===")
    upsert_variable("MY_VAR", "upserted_value")

    # Delete a variable
    print("\n=== Delete Variable ===")
    delete_variable("NEW_VAR")
