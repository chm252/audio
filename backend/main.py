from fastapi import FastAPI, File, UploadFile
import sqlite3
import whisper
import datetime
from fastapi.middleware.cors import CORSMiddleware
import tempfile

app = FastAPI()
model = whisper.load_model("tiny")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Database setup
conn = sqlite3.connect("transcriptions.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS transcriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    filename TEXT, 
                    text TEXT, 
                    timestamp TIMESTAMP)""")
conn.commit()

@app.get("/health")
def health():
    """    
    Returns a JSON response with a status message indicating 
    that the application is healthy.
    
    Returns:
    dict: A JSON object with the following structure:
        - "status" (str): "healthy"
    """

    return {"status": "healthy"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Transcribes audio into text.

    Accepts an audio file with MP3 format and transcribes it using whisper-tiny model from Hugging Face, 
    then stores the transcription in the transcriptions database.

    Parameters:
    - file (UploadFile): The audio file to be transcribed. Assuming format is MP3.

    Returns:
    dict: A JSON object with the following structure:
        - "filename" (str): The name of the uploaded file.
        - "transcription" (str): The transcribed text from the audio.
    """
    audio = await file.read()
    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
        temp_audio.write(audio)
        temp_audio.flush()

        # Transcribe with whisper-tiny
        result = model.transcribe(temp_audio.name)
        text = result["text"]    

    cursor.execute("INSERT INTO transcriptions (filename, text, timestamp) VALUES (?, ?, ?)",
                   (file.filename, text, datetime.datetime.now()))
    conn.commit()
    
    return {"filename": file.filename, "transcription": text}

@app.get("/transcriptions")
def transcriptions():
    """
    Retrives and returns all the transcriptions from the database.

    Returns:
    dict: A JSON object with the following structure:
        - "data" (str): The transcription data.
    """
    cursor.execute("SELECT * FROM transcriptions")
    data = cursor.fetchall()
    return {"data": data}

#Assuming find all whose filename's substring matches, 
#i.e. an empty string would result in return of full database since empty string is a subset of any string
@app.get("/search")
def search(query: str):
    """
    Searches for and returns the transcriptions with filename whose substring that matches the query.

    Parameters:
    - query (str): The substring to be matched

    Returns:
    dict: A JSON object with the following structure:
        - "results" (str): All the transcription data with filename that has the substring of query
    """
    cursor.execute("SELECT * FROM transcriptions WHERE filename LIKE ?", (f"%{query}%",))
    data = cursor.fetchall()
    return {"results": data}
