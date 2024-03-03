import requests
import html
import re

# Pre-compile the regular expression for extracting the UE (course unit) code.
# This pattern looks for any alphanumeric string enclosed in square brackets.
# It is used later to extract the course unit code from the event description.
ue_pattern = re.compile(r'\[(\w+)]')


def clean_description(description):
    """
    Cleans up the event description by decoding HTML entities, removing HTML tags,
    and extracting relevant information such as the event type, location, and UE (course unit) code.

    :param description: The raw HTML event description.
    :return: A dictionary with cleaned and structured event information, including type, room, and UE code.
    """
    # Decode HTML entities (like &amp;, &lt;, etc.) to get the actual characters.
    description = html.unescape(description)
    # Replace <br /> tags with newlines to simplify splitting the description into lines.
    description = description.replace('<br />', '\n')
    # Split the description into lines and remove any leading/trailing whitespace from each line.
    # Only keep lines that are not empty after stripping.
    lines = [line.strip() for line in description.split('\n') if line.strip() != '']
    description_dict = {}
    # The first line is assumed to be the event type (e.g., Lecture, Tutorial).
    if lines:
        description_dict['Type'] = lines[0]
        # The second line, if present, is assumed to be the room/location.
        if len(lines) > 1:
            description_dict['Salle'] = lines[1]
        # Search for the UE code in subsequent lines.
        # The UE code is assumed to be any alphanumeric string within square brackets.
        for line in lines[2:]:
            ue_match = ue_pattern.search(line)
            if ue_match:
                description_dict['UE'] = ue_match.group(1)  # Extract and store the UE code.
                break  # Stop searching after the first UE code is found.
    return description_dict


def parse_edt(group_id: str, start_date: str, end_date: str) -> (bool, str):
    """
    Fetches and processes the schedule from the UVSQ schedule API for a specific group within a given date range.
    Cleans the data and saves it as a JSON file.

    :param group_id: The identifier for the group whose schedule is to be fetched.
    :param start_date: The start date of the schedule in 'YYYY-MM-DD' format.
    :param end_date: The end date of the schedule in 'YYYY-MM-DD' format.
    :return: A tuple containing a boolean indicating success or failure, and a string message or the cleaned data.
    """
    # The API endpoint URL for fetching the schedule.
    url_api = 'https://edt.uvsq.fr/Home/GetCalendarData'

    # The data to be sent in the POST request to the API.
    # It includes the start and end dates, the type of resource, the calendar view type,
    # the federation ID corresponding to the group, and the color scheme for the calendar.
    data = {
        'start': start_date, 'end': end_date, 'resType': '103', 'calView': 'agendaWeek',
        'federationIds[]': group_id, 'colourScheme': '3'
    }

    # Send the POST request to the API and store the response.
    response = requests.post(url_api, data=data)

    # Process the response if the status code indicates success (200 OK).
    if response.status_code == 200:
        try:
            # Parse the JSON content of the response.
            json_data = response.json()
            # Filter and clean the data:
            # Remove unnecessary fields from each event and filter out events of type 'TP' (practical sessions).
            cleaned_data = [
                {k: v for k, v in event.items() if
                 k not in ['registerStatus', 'studentMark', 'custom1', 'custom2', 'custom3', 'department', 'textColor',
                           'backgroundColor', 'allDay', 'id', 'sites', 'eventCategory', "modules"]}
                for event in json_data if event.get('eventCategory') != 'TP'
            ]

            # Clean the description for each event using the clean_description function.
            for event in cleaned_data:
                if 'description' in event:
                    event['description'] = clean_description(event['description'])

            if not cleaned_data:
                return True, "Aucun événement n'a été trouvé pour le groupe spécifié."

            return False, cleaned_data
        except ValueError:
            # Handle cases where the response is not in valid JSON format.
            return True, "La réponse n'est pas au format JSON."
    else:
        # Handle unsuccessful responses.
        return True, "La requête a échoué avec le code d'état : " + str(response.status_code)
