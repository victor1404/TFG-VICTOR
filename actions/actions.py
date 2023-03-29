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

class ActionGoToSignIn(Action):

    def name(self) -> Text:
        return "action_go_to_sign_in"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="En caso de que no tengas cuenta puedes registrarte desde aqui: ")
        dispatcher.utter_message(attachment="https://www.decidim.barcelona/users/sign_up?locale=es")

        dispatcher.utter_message(text="\nEn caso de que ya tengas cuenta puedes iniciar sesion desde aqui ")
        dispatcher.utter_message(attachment="https://www.decidim.barcelona/users/sign_up?locale=es")

        return []

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

class ActionAPIDemo(Action):
  
    def name(self) -> Text:
        return "action_user_info"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        querys.query_user_information("Victor Llinares")

        return []  


class ActionAPI_Latest_PP(Action):
  
    def name(self) -> Text:
        return "action_latest_procesos_participativos"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response_dict = querys.query_latest_ParticipatoryProceses()
        s = response_dict["title"]["translation"]
        dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

        l = "https://www.decidim.barcelona/processes/" + response_dict["slug"]
        dispatcher.utter_template("utter_give_link", tracker, link=l)

        # dispatcher.utter_message(text="Si te interesa aqui tienes el enlace")
        # l = "https://www.decidim.barcelona/processes/" + response_dict["slug"]
        # dispatcher.utter_message(attachment=s)



        return []  