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

# Set up Azure Speech-to-Text and Text-to-Speech credentials
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("SERVICE_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_language = os.getenv("SPEECH_SYNTHESIS_LANGUAGE")
# Set up the voice configuration
speech_config.speech_synthesis_voice_name = os.getenv("SPEECH_SYNTHESIS_VOICE_NAME")

from pathlib import Path

file_system = Path("./app/content_system.txt")
system_content = file_system.read_text(encoding="utf-8")
file_assistant = Path("./app/content_assistant.txt")
assistant_content = file_system.read_text(encoding="utf-8")


def generate_message(prompt):
    response = openai.ChatCompletion.create(
        engine=os.getenv("ENGINE"),
        messages=[
            {"role": "system", "content": str(system_content)},
            {"role": "assistant", "content": str()},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
    )
    # return response["choices"][0]["message"]["content"]

    # Create SSML with prosody rate adjustment
    text = response["choices"][0]["message"]["content"]
    ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="th-TH"><voice name="th-TH-PremwadeeNeural"><prosody rate="-20.00%" volume="-50.00%" pitch="+40.00%">{text}</prosody></voice></speak>'

    # Create a speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    try:
        result = speech_synthesizer.speak_ssml(ssml)
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Text-to-speech conversion successful.")
            return text
        else:
            print(f"Error synthesizing audio: {result}")
            return False
    except Exception as ex:
        print(f"Error synthesizing audio: {ex}")
        return False
