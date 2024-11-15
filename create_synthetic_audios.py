from pathlib import Path
from google.cloud import texttospeech

BREAKING_LINE = 100000 # None if you are going to send all lines
DATASET_FILE_PATH = "common_basque_dataset.txt" # Change the dataset filename to your needs

client = texttospeech.TextToSpeechClient()
voice = texttospeech.VoiceSelectionParams(language_code="eu-ES",name="eu-ES-Standard-B",ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

with open(DATASET_FILE_PATH, "r") as dataset:
    for index, line in enumerate(dataset, 1):
        filename = "audio_{}.wav".format(index)
        path = "wav/{}".format(filename)
        myfile = Path(path)
        if not myfile.is_file():
            text = line.strip()
            input_text = texttospeech.SynthesisInput(text=text)
            try:
                response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})
                with open(path, "wb") as out:
                    out.write(response.audio_content)
                    print("✅ {}: {}".format(filename,text))
            except:
                print("❌ {}: {}".format(filename,text))
                break

        if BREAKING_LINE and index == BREAKING_LINE:
            break
