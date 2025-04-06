import requests
import yaml


def load_credentials(path="./credentials.yml"):
    with open(path, 'r') as file:
        return yaml.safe_load(file)


def generate_groq_text(system_prompt, user_query):

    grok_api_key = load_credentials().get("grok", {}).get("api_key")

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {grok_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": system_prompt},
                             {"role": "user", "content": user_query}],
                "temperature": 0.7,
                "max_tokens": 500
            }
        )

        data = response.json()
        message = data.get('choices', [{}])[0].get('message', {}).get('content', '')

        if not message:
            return "No response generated from the API."

        return message

    except Exception as e:
        return f"Error generating text: {str(e)}"


system_prompt = "Explain things in a childish manner."
user_query = "Who are you?"

print(generate_groq_text(system_prompt, user_query))

