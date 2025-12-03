# bridge-front-door
Code and work related to a front door app for refugee services.

### Problem Statement
Bridge needs a lightweight app to run on a tablet that will allow multiple spoken languages to determine if walk up clients have an appointment, whom it is with, if they are existing clients, and if it is 

MVP Requirements:
* [x] Script to create static audio files - complete
* [ ] Large buttons for language selection that go straight to a series of yes/no written/spoken questions
* [ ] Back button (for incorrect language selection) and large Yes/No (in that language) plus Green/Red and check/X on respective buttons. (See whiteboard image for rough mockups)
* [ ] Branching logic/conditional flow for questions as seen in whiteboard image
* [ ] Screen with selectable photos and names of case workers

Question/statement list:
* Welcome, we will ask you a few questions to help us support you today.
* Do you have an appointment?
* Are you an existing client?
* Do you want to schedule an appointment for later? (Answers Yes or "No - I need help today")
* One moment please.
* Please select your case worker.

### Set up
The file `create_audio_file.py` creates static files of a given English phrase in multiple languages. It has been run for the questions listed above in six languages, with messages saved in the `static` folder with a subfolder according to the message text. In order to run the script, take the following set up steps after cloning the repo.

1. Go https://cloud.google.com/vertex-ai and click "Try it in console". You will be allowed $300 free trial, which should be enough for many audio translations, but do keep an eye on billing. Also note this has different terms of service than GSuite, and no sensitive data should be shared via Vertex AI without due dilligence on data use.
2. Install the relevant google tools (`pip install --upgrade google-cloud-texttospeech` and `pip install --upgrade google-genai`). Recommend using venv prior to package installation (`python -m venv myprojectenv`, `source myprojectenv/bin/activate`) for macOS and Linux).
4. Create a service account key [here](https://console.cloud.google.com/apis/credentials/serviceaccountkey?project=YOURPROJECT) and download as a json in the home directory. Rename credentials.json for current code to work. DO NOT commit your credentials file to the git respository. Recommend using a secrets manager, especially for any deployments on VertexAI solutions.
5. On first running of the script, you may get an error message with a link to enable text to enable various APIs. You can click through and enable them in the Vertex AI console.

The file `app.py` is just an AI generated flask module to serve up static audio files. It will need editing and a lightweight front end. Other options for future state are below.

### Future State
In the future, a lightweight webapp could be made using some of the tools below, suggested by various team members at the Hackathon, to leverage the automated translations.

Low or no code hosted solutions:
* Typeform
* Google Forms

AI Assisted Coding Solutions
* Replit
* Cursor

Functional updates:
* Integration with Google calendar for each scheduling in native language (a Conversational Agents Playbook may be helpful for this)

Upgrades to translation/audio:
* Consider experimentation with various Gemini models and human SME for quality
* Consider using Google Translate API instead of Gemini - although quick research shows Gemini is likely higher quality, we have not validated for the languages and use cases specific to Bridge.

Full AI Solutions may also be relevant in the future - Google Conversational Agents has low code Playbook solutions that are multilingual and support voice. The voice to text, Gemini and Google Translate APIs will also continue to be helpful given the existing Gsuite integration, as long as any data privacy concerns can be managed.
