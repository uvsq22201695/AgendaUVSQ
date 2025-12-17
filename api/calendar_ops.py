import random

import gradio as gr

# Define a dictionary mapping event types to their corresponding color IDs.
# Google Calendar Color IDs mappings used:
# 7: Peacock (Bleu ciel)
# 4: Flamingo (Rose clair)
# 5: Banana (Jaune)
# 6: Tangerine (Jaune-orange)
# 2: Sage (Vert clair)
# 10: Basil (Vert foncé)
# 9: Blueberry (Bleu foncé - Défaut)
# 8: Grey (Gris)
EVENT_COLORS = {
    'CM': '7',  # Bleu ciel
    'Contrôle continu': '4',  # Rose clair
    'TD': '8',  # Gris
    'TD Cartable Numérique': '6',  # Jaune-orange
    'CM/TD': '2',  # Vert clair
    'Examen': '10',  # Vert foncé
}

DEFAULT_EVENT_COLOR = '9'


def get_event_color(event_type: str) -> str:
    """
    This function returns the color ID for a given event type.
    If the event type is not found in the EVENT_COLORS dictionary, it returns the default color ID.

    :param event_type: The type of the event.
    :return: The color ID as a string.
    """
    if not event_type:
        return DEFAULT_EVENT_COLOR

    normalized_type = event_type.strip()
    return EVENT_COLORS.get(normalized_type, DEFAULT_EVENT_COLOR)


def create_agenda(service, summary: str, timeZone: str) -> tuple:
    """
    This function creates a new Google Calendar with the given name.
    :param service: Google Calendar API service object.
    :param summary: Name of the new calendar.
    :param timeZone: Time zone of the new calendar.
    :return: A tuple containing a boolean indicating whether an error occurred and a string containing the calendar ID.
    """

    # Define the calendar object with its summary (name) and time zone.
    # 'summary' is the name of the new calendar.
    # 'timeZone' is the time zone of the new calendar.
    calendar = {
        "summary": summary,  # The name of the calendar to be created.
        'timeZone': timeZone  # Setting the time zone for the calendar.
    }

    # 1. Create the calendar using the Google Calendar API.
    try:
        created_calendar = service.calendars().insert(body=calendar).execute()
        calendar_id = created_calendar.get('id')
    except Exception as e:
        return True, f"Erreur API: {str(e)}"

    # 2. Optionally, set a random color for the newly created calendar.
    try:
        random_color_id = str(random.randint(1, 24))
        service.calendarList().patch(
            calendarId=calendar_id,
            body={'colorId': random_color_id}
        ).execute()
    except Exception as e:
        # Non-blocking error: Log the error but do not fail the calendar creation.
        print(f"Attention (Non bloquant) : Impossible de changer la couleur de l'agenda. {e}")

    # Return the 'id' of the created calendar.
    # The 'id' is used to uniquely identify the calendar in subsequent API calls.
    return False, created_calendar.get('id')


def callback(_, __, exception):
    """
    This function serves as a callback for batch HTTP requests.
    It is called for each individual request within a batch request.

    :param _: A unique identifier for the request within the batch.
    :param __: The response for this request. None if there was an exception.
    :param exception: The exception, if one occurred. None if the request was successful.
    """
    if exception is not None:
        gr.Warning(f"Une erreur s'est produite lors de la création de l'événement : {exception}")


def batch_create_events(service, events_data: list, calendar_id: str) -> None:
    """
    This function creates multiple calendar events in a batch request.
    Each event is created based on data from the `events_data` list.

    :param service: Google Calendar API service object.
    :param events_data: A list of dictionaries, each containing data for one event.
    :param calendar_id: The ID of the calendar where the events will be added.
    """

    # Create a new BatchHttpRequest object with the specified callback function.
    batch = service.new_batch_http_request(callback=callback)

    for event_data in events_data:
        event_type = event_data['description'].get('Type', 'Not specified')

        # Construct an event object for each item in events_data.
        event = {
            'summary': event_data['description'].get('UE', 'No title'),  # Event title
            'location': f"{event_data['description'].get('Salle', '')}, {event_data.get('faculty', '')}",
            # Event location
            'start': {
                'dateTime': event_data['start'],  # Event start time
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'dateTime': event_data['end'],  # Event end time
                'timeZone': 'Europe/Paris',
            },
            'description': f"Type: {event_type}",  # Event description
            'colorId': get_event_color(event_type),  # Event color
        }

        # Add the event creation request to the batch, specifying the calendar ID and event object.
        batch.add(service.events().insert(calendarId=calendar_id, body=event))

    # Execute the batch request. The callback function will be called for each request in the batch.
    try:
        batch.execute()
    except Exception as e:
        gr.Warning(f"Erreur lors de l'exécution du batch: {e}")
