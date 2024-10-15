from flask import Flask, request, render_template
from pytube import YouTube
import assemblyai as aai
from google.cloud import translate_v2 as translate
from flask_compress import Compress
from gtts import gTTS
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# API keys
aai.settings.api_key = "YOUR_ASSEMBLY-AI_API_KEY"
translate_client = translate.Client.from_service_account_json("YOUR_GOOGLE_CLOUD_TRANSLATE_JSON_FILE.json")
global output1

app = Flask(__name__)

Compress(app)

@app.route('/', methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route('/process_input', methods=["GET", "POST"])
def home():
    ylink = request.form.get("youtubeLink")
    yt = YouTube(ylink)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path="", filename="static/audio.mp3")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe("static/audio.mp3")
    transcripted = transcript.text
    with open("static/input.txt", "w") as srt_file:
        srt_file.write(transcripted)

    with open("static/input.srt", "w") as srt_file:
        srt_file.write(transcript.export_subtitles_srt())

    output1 = transcript.export_subtitles_srt()
        
    return output1

@app.route('/process_input2',methods=["GET", "POST"])
def translationsrt():
    with open("static/input.srt", "r") as srt_file:
        srt_content = srt_file.read()
    subtitle_entries = re.findall(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.+)\n', srt_content)
    lang = request.form.get("languagecode")
    translated_subtitles = []
    for entry in subtitle_entries:
        index, start_time, end_time, line = entry
        translation = translate_client.translate(line, target_language=lang)
        translated_subtitles.append((index, start_time, end_time, translation["translatedText"]))

    # Save the translated subtitle lines into a new SRT file
    output2 = ""  # Initialize an empty string to store the SRT content    

    for index, start_time, end_time, subtitle in translated_subtitles:
        output2 += f"{index}\n{start_time} --> {end_time}\n{subtitle}\n\n"

    return output2

@app.route('/process_input3',methods=["GET", "POST"])
def natsummary():
    lang = request.form.get("languagecode")
    with open("static/input.txt", "r") as srt_file:
        transcripted = srt_file.read()
    



    def summarize_text(text):
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        outputs = model.generate(
            inputs,
            max_length=100,  # Adjust max_length as needed
            min_length=30,   # Adjust min_length as needed
            length_penalty=1.2,
            num_beams=3,
            early_stopping=True)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
    
    def split_text(text, chunk_size=1000):
        chunks = []
        words = text.split()
        current_chunk = ''
        for word in words:
            if len(current_chunk) + len(word) < chunk_size:
                current_chunk += ' ' + word
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word
        chunks.append(current_chunk.strip())
        return chunks
    
    chunks = split_text(transcripted)
    

    # Summarize each chunk
    summaries = [summarize_text(chunk) for chunk in chunks]
    
    # Integrate the summaries into a cohesive summary
    final_summary = ' '.join(summaries)
    lang = request.form.get("languagecode")
    # Translate the final summary
    translate_client = translate.Client.from_service_account_json("learned-vehicle-413714-766132b812ea.json")
    translation = translate_client.translate(final_summary, target_language=lang)
    
    return translation["translatedText"]


@app.route('/process_input4',methods=["GET", "POST"])
def summarytts():
    lang = request.form.get("languagecode")
    text = request.form.get("text")
    tts = gTTS(text,lang=lang)
    file_path = 'static/output.mp3'
    with open(file_path, 'wb') as file:
        tts.write_to_fp(file)
    file.close

    return ''
    

if __name__ == '__main__':
    app.run(debug=True)

