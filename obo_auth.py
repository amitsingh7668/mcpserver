from msal import ConfidentialClientApplication

TENANT_ID = "xxxx"
CLIENT_ID = "AWM_APP_CLIENT_ID"
CLIENT_SECRET = "AWM_APP_SECRET"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

RESOURCE_SCOPE = ["api://AKS_API_CLIENT_ID/.default"]

app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

# user_token = token received from frontend
result = app.acquire_token_on_behalf_of(
    user_token,
    scopes=RESOURCE_SCOPE
)

obo_access_token = result["access_token"]
