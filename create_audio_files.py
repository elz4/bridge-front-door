import os
from google.cloud import texttospeech
from google import genai
from google.genai import types
##################
# TEXT TRANSLATION
##################


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "~/Workspace/bridge-front-door/credentials.json"
genai_client = genai.Client()


# Map your existing lang_key -> language name for the prompt
LANG_NAMES = {
    "en": "English",
    "sw": "Swahili",
    "es": "Spanish",
    "ar": "Arabic",
    "ru": "Russian",
    "uk": "Ukranian"
    # "fa": "Dari",        # or "Persian (Dari)" if you want to be explicit
}

def translate_text(text: str, lang_key: str) -> str:
    """
    Use Gemini API to translate *English* text to the language specified by lang_key.
    Returns the translated text as a plain string.

    lang_key must be one of LANG_NAMES keys.
    """
    if lang_key not in LANG_NAMES:
        raise ValueError(f"Unsupported lang_key: {lang_key}")

    target_lang_name = LANG_NAMES[lang_key]

    # You can swap model name (e.g., "gemini-2.5-flash" or "gemini-1.5-pro")
    prompt = (
        "You are a professional translator.\n"
        "Translate the following text from English into "
        f"{target_lang_name}.\n"
        "Return ONLY the translated text, with no explanations or notes.\n\n"
        f"Text: {text}"
    )

    response = genai_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.0,   # low temperature for more deterministic translations
            max_output_tokens=512,
        ),
    )

    # response.text is the convenience property for concatenated text parts
    translated = (response.text or "").strip()
    return translated
    

######################
# Voice File Creation
######################

# Set this to the path of your service account JSON, or export
# GOOGLE_APPLICATION_CREDENTIALS in your environment instead.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "~/Workspace/bridge-front-door/credentials.json"
client = texttospeech.TextToSpeechClient()


LANG_CONFIG = {
    "en": {"language_code": "en-US", "voice_name": None}, 
    "sw": {"language_code": "sw-KE", "voice_name": None},  # Swahili
    "es": {"language_code": "es-US", "voice_name": None},   # Spanish
    "ar": {"language_code": "ar-XA", "voice_name": None},   # Arabic (generic)
    "ru": {"language_code": "ru-RU", "voice_name": None},   # Russian
    "uk": {"language_code": "uk-UA", "voice_name": None}    # Ukranian

    # Note this configuration needs work - voice name is automatically selected 
    # for others but not here
    # "fa": {"language_code": "fa-IR", "voice_name": None},   # Persian as Dari proxy
}
def synthesize_to_mp3(text: str, lang_key: str, out_dir: str = "static/audio3") -> str:
    """
    Synthesize 'text' to an MP3 file for the language identified by lang_key.
    Returns the relative file path.
    """
    os.makedirs(out_dir, exist_ok=True)

    cfg = LANG_CONFIG[lang_key]
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice_params = {
        "language_code": cfg["language_code"],
        "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL,
    }
    if cfg["voice_name"]:
        voice_params["name"] = cfg["voice_name"]

    voice = texttospeech.VoiceSelectionParams(**voice_params)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    filename = f"message_{lang_key}.mp3"
    filepath = os.path.join(out_dir, filename)
    with open(filepath, "wb") as f:
        f.write(response.audio_content)

    # Return a path Flask can serve from /static
    return f"/static/audio/{filename}"


if __name__ == "__main__":
    MESSAGES_DIR_NAMES = {
        "static/welcome": "Welcome. We will ask you a few questions to help us support you today",
        "static/appt": "Do you have an appointment?",
        "static/client": "Are you an existing client?",
        "static/today": "Do you want to make an appointment for later?", # Envisioning an answer of "No I need help immediately"
        "static/wait": "One moment please.",
        "static/worker": "Please select your case worker."
    }

    TARGET_LANG_KEYS = ["en", "sw", "es", "ar", "ru", "uk"] #, "fa"]

    def build_all_messages(english_msg, out_dir):
      for lang_key in TARGET_LANG_KEYS:
          if lang_key == "en":
              text = english_msg
          else:
              text = translate_text(english_msg, lang_key)
          url_path = synthesize_to_mp3(text, lang_key, out_dir=out_dir)
          print(lang_key, "->", url_path)

    for out_dir, eng_msg in MESSAGES_DIR_NAMES.items():
        build_all_messages(eng_msg, out_dir)

