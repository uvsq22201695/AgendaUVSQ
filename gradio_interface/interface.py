import datetime

import gradio as gr
from gradio_calendar import Calendar

from api.auth import get_api
from api.calendar_ops import batch_create_events
from api.calendar_ops import create_agenda
from data.edt_parser import parse_edt


def make_model():
    """
    Crée l'interface graphique
    """

    with gr.Blocks() as iface:
        gr.Markdown("# Agenda UVSQ")

        gr.Markdown("Récupérer les données de l'emploi du temps et les mettre dans un agenda Google.")

        def check_values(groupID: str, startDate: datetime.datetime, endDate: datetime.datetime):
            """
            Vérifie que les valeurs entrées sont valides.
            :param groupID: ID du groupe.
            :param startDate: Date de début.
            :param endDate: Date de fin.
            """

            if not groupID:
                return gr.Warning("Veuillez entrer l'ID du groupe.")
            if not startDate:
                return gr.Warning("Veuillez entrer la date de début.")
            if not endDate:
                return gr.Warning("Veuillez entrer la date de fin.")
            if startDate > endDate:
                return gr.Warning("La date de début doit être antérieure à la date de fin.")

            # Conversion explicite en string pour l'API UVSQ
            err_bool_edt, edt_data = parse_edt(groupID, startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'))

            if err_bool_edt:
                return gr.Warning(edt_data)

            gr.Info("Connexion aux services Google...")
            err_bool_api, api_data = get_api()

            if err_bool_api:
                return gr.Warning(api_data)

            gr.Info("Création/Mise à jour de l'agenda...")
            err_bool_agenda, agenda_id = create_agenda(api_data, f"UVSQ Agenda {groupID}", "Europe/Paris")

            if err_bool_agenda:
                return gr.Warning(agenda_id)

            gr.Info(f"Ajout des {len(edt_data)} événements...")
            batch_create_events(api_data, edt_data, agenda_id)
            gr.Info(f"Succès ! L'agenda 'UVSQ Agenda {groupID}' a été mis à jour avec {len(edt_data)} événements.")
            return None

        with gr.Column():
            group_id = gr.Textbox(label="ID du groupe", type="text", placeholder="M1 Info gr. 1", max_lines=1)

            with gr.Row():
                start_date = Calendar(type="datetime", label="Date de début",
                                      info="Cliquez sur l'icône du calendrier pour afficher le calendrier.")
                end_date = Calendar(type="datetime", label="Date de fin",
                                    info="Cliquez sur l'icône du calendrier pour afficher le calendrier.")

            submit_btn = gr.Button(value="Lancer l'importation", variant="primary")

            submit_btn.click(fn=check_values, inputs=[group_id, start_date, end_date])

        iface.launch()
