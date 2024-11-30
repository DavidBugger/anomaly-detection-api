import requests
from config import Config
def get_access_token():
    """Fetch an access token for Microsoft Graph API."""
    data = {
        "grant_type": "client_credentials",
        "client_id": Config.CLIENT_ID,
        "client_secret": Config.CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
    try:
        response = requests.post(Config.TOKEN_URL, data=data)
        print("Token Request Status Code:", response.status_code)
        print("Token Request Response Body:", response.text)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e.response.status_code}, {e.response.text}")
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise


def fetch_sign_in_logs():
    """Fetch Azure AD sign-in logs using Microsoft Graph API."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://graph.microsoft.com/v1.0/auditLogs/signIns"
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        raise Exception("Failed to fetch sign-in logs.")



# def fetch_logs():
#     """Fetch Azure AD logs using Microsoft Graph API."""
#     token = get_access_token()
#     headers = {"Authorization": f"Bearer {token}"}
#     response = requests.get(Config.GRAPH_API_URL, headers=headers)
#     response.raise_for_status()
#     return response.json()["value"]

# def fetch_logs():
#     headers = {"Authorization": f"Bearer {Config.MS_GRAPH_API_TOKEN}"}
#     response = requests.get(Config.GRAPH_API_URL, headers=headers)
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch logs: {response.text}")
#     return response.json()

def fetch_logs():
    try:
        token = get_access_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(Config.GRAPH_API_URL, headers=headers)
        response.raise_for_status()
        return response.json()["value"]
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            raise Exception("Permission denied. Check API permissions in Azure.")
        elif e.response.status_code == 401:
            raise Exception("Authentication failed. Check client ID, secret, or tenant ID.")
        else:
            raise
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

