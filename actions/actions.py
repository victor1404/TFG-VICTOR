# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
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


ALLOWED_LOCATIONS = ["Ciutat Vella", "Eixample", "Sants", "Sarria", "Sant Gervasi", "Les Corts", "Gracia", "Horta", "Guinardó", "Nou Barris", "Sant Andreu", "Sant Martí"]

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


class ActionGET_ParticipatoryeProcess(Action):
    
    def name(self) -> Text:
        return "action_procesos_participativos"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # response_dict = querys.query_latest_ParticipatoryProceses()
        # s = response_dict["title"]["translation"]
        # dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

        # l = "https://www.decidim.barcelona/processes/" + response_dict["slug"]
        # dispatcher.utter_template("utter_give_link", tracker, link=l)

        # return [] 
        neighborhood = next(tracker.get_latest_entity_values("neighborhood_location"), None) 

        if neighborhood is None:
            # no nos ha proporcionado un lugar. 
            response_dict = querys.query_latest_ParticipatoryProceses()
            title = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: **{title}**")               

            slug = response_dict["slug"]
            l = "https://www.decidim.barcelona/processes/" + slug
            dispatcher.utter_template("utter_give_link", tracker, link=l)
            return [SlotSet("actual_slug_PP", slug)]

        else:

            if neighborhood.title() not in ALLOWED_LOCATIONS:
                dispatcher.utter_message("Eso no sirve, la localizacion debe ser :")
                dispatcher.utter_message("Ciutat Vella, Eixample, Sants, Sarria, Sant Gervasi, Les Corts, Gracia, Horta, Guinardó, Nou Barris, Sant Andreu o Sant Martí.")
                return []

            response_dict = querys.query_ParticipatoryProceses_location(neighborhood)
            title = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"He intentado buscar cerca de {neighborhood}")
            dispatcher.utter_message(text=f"He encontrado esto: {title}")

            slug = response_dict["slug"]
            l = "https://www.decidim.barcelona/processes/" + slug
            
            if title == "Reurbanización de los interiores de manzana de la Guineueta":
                l = "Reurbanización de los interiores de manzana de la Guineueta - decidim.barcelona.html"
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [SlotSet("actual_slug_PP", slug)]


class ActionLOOK_ParticipatoryeProcess(Action):

    def name(self) -> Text:
        return "action_mirar_en_proceso_participativo"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        slug = tracker.get_slot("actual_slug_PP") 
        print(intent)
        print(tracker.latest_message['entities'])
        if slug is None:
            dispatcher.utter_message("No sé a que proceso participativo te refieres")
            return []

        if intent == "debate_in_participatory_process":
            SlotSet("interests", "Debates")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Debates"):
                    dispatcher.utter_message("Sí, el proceso tiene debate")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene debate")
            return []

        elif intent == "meeting_in_participatory_process":
            SlotSet("interests", "Meetings")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Meetings"):
                    dispatcher.utter_message("Sí, el proceso tiene encuentros")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene encuentros")
            return []

        elif intent == "proposals_in_participatory_process":
            SlotSet("interests", "Proposals")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Proposals"):
                    dispatcher.utter_message("Sí, el proceso tiene propuestas")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene propuestas")
            return []

        elif intent == "budgets_in_participatory_process":
            SlotSet("interests", "Budgets")
            componentes = querys.query_Components_ParticipatoryProceses(slug)

            for component in componentes:
                if (component['__typename'] == "Budgets"):
                    dispatcher.utter_message("Sí, el proceso tiene presupuestos")

                    id = component["id"]
                    l = "https://www.decidim.barcelona/processes/" + slug +"/f/"+id
                    dispatcher.utter_template("utter_give_link", tracker, link=l)
                    return []
            
            dispatcher.utter_message("Parece que no tiene presupuestos")
            return []



    
    








    class ActionAPI_Latest_Debate(Action):
    
        def name(self) -> Text:
            return "action_latest_Debate"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            response_dict = querys.query_Debates()
            s = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response_dict["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return []  


    class ActionAPI_Latest_Survey(Action):
    
        def name(self) -> Text:
            return "action_latest_Survey"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            response_dict = querys.query_Surveys()
            s = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response_dict["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [] 


    class ActionAPI_Latest_Budget(Action):
    
        def name(self) -> Text:
            return "action_latest_Budget"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            response_dict = querys.query_Budgets()
            s = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response_dict["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return []  


    class ActionAPI_Latest_Proposal(Action):
  
        def name(self) -> Text:
            return "action_latest_Proposal"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            response_dict = querys.query_Proposals()
            s = response_dict["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response_dict["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return []



# QUERYS CON LOCATION

    class ActionAPI_Debate_Location(Action):
    
        def name(self) -> Text:
            return "action_debate_location"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            ent = tracker.latest_message['entities'][0]['value']    
            # slot_value = str(tracker.get_slot('neighborhood_location'))
            response_dict = querys.query_Debate_location()
            response = response_dict[0]
            found = False
            
            for d in response_dict:
                if not found:
                    if ent in d["title"]["translation"] or ent in d["description"]["translation"] or ent in d["localArea"]["translation"]:
                        found = True
                        response = d
                    

            s = response["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [] 


    class ActionAPI_Surveys_Location(Action):
    
        def name(self) -> Text:
            return "action_surveys_location"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            ent = tracker.latest_message['entities'][0]['value']    
            # slot_value = str(tracker.get_slot('neighborhood_location'))
            response_dict = querys.query_Surveys_location()
            response = response_dict[0]
            found = False
            
            for d in response_dict:
                if not found:
                    if ent in d["title"]["translation"] or ent in d["description"]["translation"] or ent in d["localArea"]["translation"]:
                        found = True
                        response = d
                    

            s = response["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [] 


    class ActionAPI_Budget_Location(Action):
    
        def name(self) -> Text:
            return "action_budget_location"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            ent = tracker.latest_message['entities'][0]['value']    
            # slot_value = str(tracker.get_slot('neighborhood_location'))
            response_dict = querys.query_Budget_location()
            response = response_dict[0]
            found = False
            
            for d in response_dict:
                if not found:
                    if ent in d["title"]["translation"] or ent in d["description"]["translation"] or ent in d["localArea"]["translation"]:
                        found = True
                        response = d
                    

            s = response["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [] 


    class ActionAPI_Proposal_Location(Action):
  
        def name(self) -> Text:
            return "action_proposal_location"

        def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            ent = tracker.latest_message['entities'][0]['value']    
            # slot_value = str(tracker.get_slot('neighborhood_location'))
            response_dict = querys.query_Proposal_location()
            response = response_dict[0]
            found = False
            
            for d in response_dict:
                if not found:
                    if ent in d["title"]["translation"] or ent in d["description"]["translation"] or ent in d["localArea"]["translation"]:
                        found = True
                        response = d
                    

            s = response["title"]["translation"]
            dispatcher.utter_message(text=f"Te recomiendo el proceso: {s}")

            l = "https://www.decidim.barcelona/processes/" + response["slug"]
            dispatcher.utter_template("utter_give_link", tracker, link=l)

            return [] 




class ValidateSimpleLocationForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_simple_location_form"

    def validate_neighborhood_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `neighborhood_location` value."""

        print(slot_value)

        if slot_value.lower() not in ALLOWED_LOCATIONS:
            dispatcher.utter_message(text=f"Esa localizacion no sirve. Debe ser Horta o Gracia.")
            return {"neighborhood_location": None}
        dispatcher.utter_message(text=f"OK! guardamos el valor {slot_value}.")
        return {"neighborhood_location": slot_value}

class ActionValidarNeighbor(Action):

    def name(self) -> Text:
        return "action_validar_neighbor"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        neighborhood = next(tracker.get_latest_entity_values("neighborhood_location"), None)
        slot = tracker.get_slot("neighborhood_location")
        print("\nSlot:")
        print(slot)
        print("neighbor:")
        print(neighborhood)
        if slot is not None:
            dispatcher.utter_template("utter_change_location", tracker, neighborhood_location=slot)
            return [SlotSet("new_neighborhood_location", neighborhood)]


        if neighborhood.title() not in ALLOWED_LOCATIONS:
            dispatcher.utter_message("Eso no sirve, la localizacion debe ser :")
            dispatcher.utter_message("Ciutat Vella, Eixample, Sants, Sarria, Sant Gervasi, Les Corts, Gracia, Horta, Guinardó, Nou Barris, Sant Andreu o Sant Martí.")
            return []
        else:
            dispatcher.utter_message(text=f"Me acordaré que te interesa {neighborhood}.")
            return [SlotSet("neighborhood_location", neighborhood)]

class ActionChangeNeighbor(Action):

    def name(self) -> Text:
        return "action_change_neighbor"

    def run(self, dispatcher: CollectingDispatcher,
    tracker: Tracker,
    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        neighborhood = next(tracker.get_latest_entity_values("neighborhood_location"), None)
        print("\nEntity:")
        print(neighborhood)
        if neighborhood is None:
            slot = tracker.get_slot("new_neighborhood_location")
            print("Slot:")
            print(slot)
            return [SlotSet("neighborhood_location", slot)]
        return [SlotSet("neighborhood_location", neighborhood)]
