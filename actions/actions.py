from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        events = [SessionStarted(), ActionExecuted("action_listen")]
        dispatcher.utter_message(text="Hi there! I'm your personal board game chatbot.\n"
                                      "You can ask me some questions about the rules of your favorite board game and "
                                      "I will try my best to answer them.\n"
                                      "How can I help you today?")

        return events


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
