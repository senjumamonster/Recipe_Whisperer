import os
import requests

api_key = os.environ.get("GNANI_API_KEY")
tts_url = "https://api.vachana.ai/api/v1/tts/inference"

headers = {
    "X-API-Key-ID": api_key,
    "Content-Type": "application/json"
}

payload = {
    "text": "Hello Subiksha, your Gnani AI setup is working successfully.",
    "voice": "Nalini",
    "model": "timbre-v2.5",
    "language": "hi-IN"
}

response = requests.post(tts_url, headers=headers, json=payload)

if response.status_code == 200:
    with open("test_output.wav", "wb") as f:
        f.write(response.content)
    print("SUCCESS! Saved test_output.wav")
else:
    print("ERROR:", response.status_code, response.text)