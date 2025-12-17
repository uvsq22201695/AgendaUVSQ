import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for the Google Calendar API; this determines what permissions your app will have.
SCOPES = ["https://www.googleapis.com/auth/calendar.app.created"]


def get_api() -> tuple:
    """
    Establishes a connection to the Google Calendar API.

    Returns:
        A tuple where the first element is a boolean indicating if an error occurred
        (True for an error, False for success), and the second element is either
        the service object for successful connections or an error message string.
    """

    # Check if the credentials file exists.
    if not os.path.exists("credentials.json"):
        return True, "Fichier 'credentials.json' manquant à la racine du projet."

    try:
        # Initialize the OAuth2 flow controller with the client secrets and the desired scopes.
        # 'credentials.json' should be obtained from the Google Cloud Console for your project.
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)

        # Run the local server flow to authenticate the user and obtain access tokens.
        # This opens a new browser window for the user to log in and authorize the app.
        creds = flow.run_local_server(port=0)

        # Build the service object for the Google Calendar API using the obtained credentials.
        service = build("calendar", "v3", credentials=creds)

        # Return False (no error) and the service object if the connection is successful.
        return False, service

    except HttpError as error:
        # Return True (error occurred) and the error message.
        return True, f"Une erreur s'est produite : {error}"
    except Exception as e:
        # Return True (error occurred) and the error message.
        return True, f"Erreur inattendue : {e}"
