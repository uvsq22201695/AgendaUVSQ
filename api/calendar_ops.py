import gradio as gr


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

    # Use the Google Calendar API service to insert a new calendar.
    # The 'insert' method is called on the 'calendars' resource of the service object,
    # passing the 'calendar' object as the request body.
    # The 'execute' method sends the request to the server and returns the response.
    created_calendar = service.calendars().insert(body=calendar).execute()

    if created_calendar is None:
        return True, "Une erreur s'est produite lors de la création de l'agenda."

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

    # Define a dictionary mapping event types to their corresponding color IDs.
    colors = {
        'CM': '1',  # Light blue
        'Contrôle continu': '4',  # Pink
        'TD Cartable Numérique': '8',  # Grey
        'TD': '8',  # Grey
    }

    # Create a new BatchHttpRequest object with the specified callback function.
    batch = service.new_batch_http_request(callback=callback)

    for event_data in events_data:
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
            'description': f"Type: {event_data['description'].get('Type', 'Not specified')}",  # Event description
            'colorId': colors.get(event_data['description'].get('Type', 'Not specified'), None),  # Event color
        }

        # Add the event creation request to the batch, specifying the calendar ID and event object.
        batch.add(service.events().insert(calendarId=calendar_id, body=event))

    # Execute the batch request. The callback function will be called for each request in the batch.
    batch.execute()
