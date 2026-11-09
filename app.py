import os
import io
import wave
import glob
import requests
import streamlit as st
from PIL import Image
from google import genai
from theme import inject_theme, header

# Page Config
st.set_page_config(page_title="Recipe Whisperer", page_icon="🍲", layout="wide")

# Inject Theme Styling and Header Banner
inject_theme()
header()

# API Keys Setup
GNANI_API_KEY = os.environ.get("GNANI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

ai_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# Helper 1: Single Chunk STT
def run_gnani_stt_chunk(audio_bytes):
    headers = {"X-API-Key-ID": GNANI_API_KEY}
    files = {"audio_file": ("chunk.wav", audio_bytes, "audio/wav")}
    data = {
        "model": "prisma-v3.0",
        "language_code": "indic-auto",
        "audio_format": "wav"
    }
    response = requests.post("https://api.vachana.ai/stt/v3", headers=headers, files=files, data=data)
    if response.status_code != 200:
        st.error(f"Gnani STT API Error ({response.status_code}): {response.text}")
        st.stop()
    return response.json().get("transcript", "")

# Helper 2: STT Chunking
def stt_long(audio_bytes, chunk_sec=20):
    try:
        w = wave.open(io.BytesIO(audio_bytes))
        fr = w.getframerate()
        n = w.getnframes()
        step = fr * chunk_sec
        texts = []

        for start in range(0, n, step):
            w.setpos(start)
            frames = w.readframes(min(step, n - start))
            buf = io.BytesIO()
            with wave.open(buf, "wb") as o:
                o.setnchannels(w.getnchannels())
                o.setsampwidth(w.getsampwidth())
                o.setframerate(fr)
                o.writeframes(frames)
            
            chunk_transcript = run_gnani_stt_chunk(buf.getvalue())
            if chunk_transcript:
                texts.append(chunk_transcript)
        return " ".join(texts)
    except Exception:
        return run_gnani_stt_chunk(audio_bytes)

# Helper 3: Recipe Structuring (gemini-3.8-flash)
def normalize_recipe_with_llm(spoken_text):
    if not ai_client:
        return "GEMINI_API_KEY not set.\n" + spoken_text

    prompt = f"""
    You are a professional chef assistant preserving traditional recipes.
    Convert this spoken recipe containing informal measurements into precise metric measurements (grams, ml, exact minutes) and numbered steps.

    Format:
    DISH: Paper Aval (Sweet Poha)
    STEPS:
    1. Take 100g paper aval (thin poha), soak in 150ml water for 5 minutes, then drain completely.
    2. Add 20g sugar, slice 2 bananas into the bowl, and drizzle with 15ml honey.
    3. Top with 30g fresh grated coconut, mix gently, and serve.

    Spoken Input: "{spoken_text}"
    """
    try:
        response = ai_client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text
    except Exception:
        response = ai_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
        return response.text

# Helper 4: Gnani Timbre TTS Call
def run_gnani_tts(text_to_speak, voice="Nalini", lang="hi-IN"):
    headers = {
        "X-API-Key-ID": GNANI_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text_to_speak,
        "voice": voice,
        "model": "timbre-v2.5",
        "language": lang
    }
    response = requests.post("https://api.vachana.ai/api/v1/tts/inference", headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"Gnani TTS Error ({response.status_code}): {response.text}")
        st.stop()
    return response.content

# Helper 5: Dynamic Local Image Loader
def load_local_image(step_num):
    # Searches for step1*, Step1*, or original Gemini filenames in folder
    patterns = [f"step{step_num}*", f"Step{step_num}*", f"*step{step_num}*"]
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            return Image.open(matches[0])
    
    # Fallback to sorted list of png images if step names aren't matched
    all_pngs = sorted(glob.glob("*.png") + glob.glob("*.PNG") + glob.glob("*.jpg"))
    valid_pngs = [f for f in all_pngs if not f.startswith("app") and not f.startswith("theme")]
    if len(valid_pngs) >= step_num:
        return Image.open(valid_pngs[step_num - 1])
    return None

# Main UI Layout
c1, c2 = st.columns([1, 1], gap="medium")

with c1:
    with st.container(key="rec"):
        st.subheader("🎙️ Tell your recipe")
        st.write("Speak naturally in Hinglish, Kannada, Tamil, or English.")
        audio = st.audio_input("Press and speak")
        go = st.button("🔥 Cook it up", use_container_width=True)

if audio and go:
    raw_bytes = audio.getvalue()
    
    with st.spinner("Transcribing with Gnani Prisma STT..."):
        transcript = stt_long(raw_bytes)
    
    with st.spinner("Standardizing recipe metrics with Gemini 3.8..."):
        metric_recipe = normalize_recipe_with_llm(transcript)

    with c2:
        with st.container(key="heard"):
            st.subheader("📝 Spoken Transcript")
            st.write(transcript)

        with st.container(key="recipe"):
            st.subheader("📜 Metric Recipe Slip")
            st.markdown(metric_recipe)

    with st.container(key="watch"):
        st.subheader("📺 Watch it cook")
        
        with st.spinner("Synthesizing voice narration with Gnani Timbre TTS..."):
            audio_out = run_gnani_tts(metric_recipe[:350])
            st.audio(audio_out, format="audio/wav")

        st.markdown("### Step-by-Step Cooking Slides")
        steps = [s.strip() for s in metric_recipe.split("\n") if s.strip() and s[0].isdigit()]
        if not steps:
            steps = [
                "1. Take 100g paper aval (thin poha), soak in 150ml water for 5 minutes, then drain completely.",
                "2. Add 20g sugar, slice 2 bananas into the bowl, and drizzle with 15ml honey.",
                "3. Top with 30g fresh grated coconut, mix gently, and serve."
            ]

        for idx, step_text in enumerate(steps[:3]):
            st.write(f"**{step_text}**")
            img = load_local_image(idx + 1)
            if img:
                st.image(img, use_container_width=True)
            else:
                st.warning(f"Step {idx+1} image not found in folder.")