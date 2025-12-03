from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Language metadata for the UI
LANGS = {
    "en": {"label": "English",  "audio": "/static/audio/message_en.mp3"},
    "sw": {"label": "Swahili",  "audio": "/static/audio/message_sw.mp3"},
    "es": {"label": "Spanish",  "audio": "/static/audio/message_es.mp3"},
    "ar": {"label": "Arabic",   "audio": "/static/audio/message_ar.mp3"},
    "ru": {"label": "Russian",  "audio": "/static/audio/message_ru.mp3"},
    "fa": {"label": "Dari/Farsi", "audio": "/static/audio/message_fa.mp3"},
}

# Same text as in generate_tts.py, kept in sync
MESSAGES = {
    "en": "Welcome. We will ask you a few questions to help us support you today.",
    "sw": "Karibu. Tutakuuliza maswali machache ili kutusaidia tukuhudumie leo.",
    "es": "Bienvenido. Le haremos algunas preguntas para poder ayudarle hoy.",
    "ar": "مرحباً. سنطرح عليك بعض الأسئلة لمساعدتنا على دعمك اليوم.",
    "ru": "Добро пожаловать. Мы зададим вам несколько вопросов, чтобы лучше помочь вам сегодня.",
    "fa": "خوش آمدید. چند سوال از شما می‌پرسیم تا امروز بهتر بتوانیم به شما کمک کنیم.",
}

@app.route("/")
def select_language():
    # Language selection screen
    return render_template("select_language.html", langs=LANGS)

@app.route("/screen/<lang_code>")
def question_screen(lang_code):
    if lang_code not in LANGS:
        return redirect(url_for("select_language"))

    message = MESSAGES[lang_code]
    audio_url = LANGS[lang_code]["audio"]
    label = LANGS[lang_code]["label"]
    return render_template(
        "question_screen.html",
        lang_code=lang_code,
        label=label,
        message=message,
        audio_url=audio_url,
    )

@app.route("/answer", methods=["POST"])
def record_answer():
    lang_code = request.form.get("lang_code", "en")
    answer = request.form.get("answer")  # "yes" or "no"

    # TODO: store or route the answer as needed (DB, log file, webhook, etc.)
    print(f"Answer from lang={lang_code}: {answer}")

    # For now, redirect to language selection or a thank-you screen
    return redirect(url_for("select_language"))

if __name__ == "__main__":
    # Use host="0.0.0.0" on a LAN kiosk, debug=False in production
    app.run(host="0.0.0.0", port=5000, debug=True)
