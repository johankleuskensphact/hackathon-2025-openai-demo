import requests

class ChatClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def send_message(self, user_input: str = "") -> str:
        url = f"{self.base_url}/chat"
        try:
            message_req = {
                "context": {
                    "overrides": {
                        "gpt4v_input": "textAndImages",
                        "retrieval_mode": "hybrid",
                        "semantic_captions": False,
                        "semantic_ranker": True,
                        "suggest_followup_questions": True,
                        "top": 3,
                        "use_gpt4v": False,
                        "use_groups_security_filter": False,
                        "use_oid_security_filter": False,
                        "vector_fields": ["embedding"],
                        "include_category": "puurbaarlo"
                    }
                },
                "messages" :[
                    {"content": user_input,
                    "role": "user"}
                ],
                "session_state": None,
                "stream": False
            }

            response = requests.post(url, json=message_req)  # Add user_input later if needed
            response.raise_for_status()
            data = response.json()
            message = data.get("message", "No message in response.")
            return message
        except requests.RequestException as e:
            return f"Request error: {e}"
        

