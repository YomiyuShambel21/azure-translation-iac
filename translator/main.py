import os
import requests
from dotenv import load_dotenv

# Load API credentials
load_dotenv("config.env")

KEY = os.getenv("TRANSLATOR_KEY")
ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
REGION = os.getenv("TRANSLATOR_REGION")

headers = {
    "Ocp-Apim-Subscription-Key": KEY,
    "Ocp-Apim-Subscription-Region": REGION,
    "Content-Type": "application/json"
}

def translate_text(text, to_lang="fr"):
    url = f"{ENDPOINT}/translate?api-version=3.0&to={to_lang}"
    body = [{"text": text}]

    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]

if __name__ == "__main__":
    file_path = "../sample_input/sample.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        original = f.read()
        print("\n🔄 Original:", original)

        translated = translate_text(original)
        print("\n✅ Translated:", translated)

        # Save translated version
        with open("translated.txt", "w", encoding="utf-8") as out:
            out.write(translated)
        print("\n📁 Saved: translated.txt")
