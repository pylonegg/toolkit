import requests
import json
from pylonegg.automation.outlook import read_inbox, create_draft_email
from pylonegg.automation.prompts import *
from pylonegg.config import load_config
from pylonegg.database import save_task
import logging



# Load API key
config  = load_config()
model   = config["openai_model"]
api_key = config["openai_api_key"]

def sender(prompt, model=model):
    """Send a prompt to OpenAI API and return text output."""
    try:
        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={"model": model, "input": prompt},
            verify=False
        )
        response.raise_for_status()
        data = response.json()

        if "output" in data and len(data["output"]) > 0:
            return "".join([item.get("content", [{}])[0].get("text", "") for item in data["output"]]).strip()
        return ""
    except requests.exceptions.RequestException as e:
        print("HTTP Request failed:", e)
        return ""
    except Exception as e:
        print("Error parsing response:", e)
        return ""



def prompt(prompt, payload):
    load = f"""{prompt}\n\nemail:\n\n{payload}"""
    output = str(sender(load))
    return output


def main():
        print("Checking inbox...")
        emails = read_inbox()

        for email in emails:
            # Ask AI if this email requires a reply
            needs_reply = prompt(prompt_decide_actions, email['body']).strip().upper()
            
            logging.info(f"Email from {email['subject']} - Needs reply? {needs_reply}")

            if needs_reply in ["YES", "TASKS"]:
                # Generate draft reply
                draft = prompt(prompt_generate_reply, email['body'])
                logging.info(f"Creating draft for {email['sender']}:\n{email['subject']}\n")
                create_draft_email(email['object_ref'], draft)
            else:
                logging.info(f"No reply needed for email from {email['sender']}:\n{email['subject']}\n")