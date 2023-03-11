# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import querys

definiciones = {
    "procesos participativos" : "Los procesos participativos son una serie de encuentros delimitados en un tiempo concreto para promover el debate y el contraste de argumentos entre la ciudadanía, o entre ésta y las personas responsables municipales."
    ,"organos de participacion" : "Los órganos de participación son canales de encuentro y de interlocución regulares entre la ciudadanía y el Ayuntamiento para debatir y recoger opiniones y propuestas con el fin de incidir en las políticas municipales. "
    ,"inciativas ciudadanas" : "La iniciativa ciudadana es el medio que tiene la ciudadanía para promover, a través de la recogida de firmas, que el Ayuntamiento lleve a cabo una determinada acción de interés colectivo, siempre que esté dentro de sus competencias."
    ,"registrar" : "Un registro informático es un tipo o conjunto de datos almacenados en un sistema "
    ,"iniciar sesion" : "La sesión informática suele incluir el intercambio de paquetes de información entre un usuario y un servidor. Es habitual que el usuario deba ingresar un nombre de usuario y contraseña para iniciar una sesión, en un procedimiento conocido como log in o loguearse."
    ,"debate" : "Espacios digitales para informarte y decidir sobre las propuestas de cada proceso."
    ,"votacion" : "Acción de votar."
    ,"encuentros" : "Encuentros cara a cara vinculados a los procesos de cada territorio o ámbito."
    ,"propuestas" : "Contribuciones de los participantes que pueden recibir el apoyo de los usuarios con función decisoria."
    ,"presupuesto" : "Cálculo anticipado del coste de una obra o un servicio. "
    ,"consejo de barrio" : "Los Consejos de Barrio son órganos para la participación de los vecinos en el desarrollo de la ciudad, basados en la división territorial del término municipal en barrios."
    ,"comentarios" : "Contribuciones de los usuarios al hilo de una propuesta o debate y que pueden recibir una votación negativa o positiva."

}

class ActionDevolverDebates(Action):

    def name(self) -> Text:
        return "action_return_debates"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        neighborhood = tracker.get_slot("neighborhood")
        dispatcher.utter_message(text=f"Estos son los debates en {neighborhood}a los que te puedes unir:")
        
        if not neighborhood:
            dispatcher.utter_message(text=f"No sabemos en que zona estás mas interesada. Igualmente estos son los debates mas populares:")
        else:
            dispatcher.utter_message(text=f"Estos son los debates en {neighborhood} a los que te puedes unir:")

        return []


class ActionGoToPage(Action):

    def name(self) -> Text:
        return "action_go_to_page"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        dispatcher.utter_message(attachment="urldestion.com")

        return []

# class ActionReturnDefinition(Action):

#     def name(self) -> Text:
#         return "action_definition"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # concept = tracker.get_latest_entity_values("concept")
#         concept = tracker.latest_message['entities'][0]['value']
#         dispatcher.utter_message(text=f"Definicion sobre {concept}: {definiciones[concept]}")

#         return []


class ActionDisplayButtons(Action):

    def name(self) -> Text:
        return "action_yes_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(buttons = [
                {"payload": "/affirm", "title": "Yes"},
                {"payload": "/deny", "title": "No"},
            ])

        return []



class ActionPicker(Action):

    def name(self) -> Text:
        return "action_picker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        date_picker = {
            "blocks":[
                {
                "type": "section",
                "text":{
                    "text": "Make a bet on when the world will end:",
                    "type": "mrkdwn"
                },
                "accessory":
                {
                    "type": "datepicker",
                    "initial_date": "2019-05-21",
                    "placeholder":
                    {
                    "type": "plain_text",
                    "text": "Select a date"
                    }
                }
                }
            ]
            }
        dispatcher.utter_message(json_message = date_picker)

        return []

class ActionAPI(Action):

    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city="Barcelona"
        temp=int(querys.weather(city)['temp']-273)
        dispatcher.utter_template("utter_temp",
            tracker,temp=temp)

        return []