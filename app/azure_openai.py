import os
import azure.cognitiveservices.speech as speechsdk
import openai
from dotenv import load_dotenv

load_dotenv()

# Set up Azure OpenAI API credentials
openai.api_type = "azure"
openai.api_base = os.getenv("API_BASE")
openai.api_version = os.getenv("API_VERSION")
openai.api_key = os.getenv("API_KEY")


from pathlib import Path

file_system = Path("./app/content/content_system.txt")
system_content = file_system.read_text(encoding="utf-8")

file_assistant_women = Path("./app/content/content_assistant_women.txt")
assistant_content_women = file_assistant_women.read_text(encoding="utf-8")

file_assistant_men = Path("./app/content/content_assistant_men.txt")
assistant_content_men = file_assistant_men.read_text(encoding="utf-8")


def generate_message(prompt, voice):
    if voice == "women":
        response = openai.ChatCompletion.create(
            engine=os.getenv("ENGINE"),
            messages=[
                {"role": "system", "content": str(system_content)},
                {"role": "assistant", "content": str(assistant_content_women)},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
    else:
        response = openai.ChatCompletion.create(
            engine=os.getenv("ENGINE"),
            messages=[
                {"role": "system", "content": str(system_content)},
                {"role": "assistant", "content": str(assistant_content_men)},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
    data = response["choices"][0]["message"]["content"]
    return data
