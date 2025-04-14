from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from textblob import TextBlob
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
import cv2
import numpy as np
from deepface import DeepFace
from enum import Enum
from typing import List, Dict, Any
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Multimodal Sentiment Analysis API")

# ✅ Add CORS correctly before adding routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:3000"] in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    AMBIVALENT = "ambivalent"

class SentimentScore(BaseModel):
    sentiment: SentimentType
    confidence: float

class SentimentResponse(BaseModel):
    text_sentiment: SentimentScore
    audio_sentiment: SentimentScore
    visual_sentiment: SentimentScore
    combined_sentiment: SentimentScore
    is_ambivalent: bool
    details: Dict[str, Any]

def analyze_text_sentiment(file_content: bytes) -> SentimentScore:
    text = file_content.decode(errors="ignore")
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = SentimentType.POSITIVE
    elif polarity < -0.1:
        sentiment = SentimentType.NEGATIVE
    else:
        sentiment = SentimentType.NEUTRAL
    confidence = round(abs(polarity), 2)
    return SentimentScore(sentiment=sentiment, confidence=confidence)

def analyze_audio_sentiment(file_content: bytes) -> SentimentScore:
    try:
        audio = AudioSegment.from_file(BytesIO(file_content))
        audio.export("temp.wav", format="wav")
        recognizer = sr.Recognizer()
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return analyze_text_sentiment(text.encode())
    except Exception:
        return SentimentScore(sentiment=SentimentType.NEUTRAL, confidence=0.5)

def analyze_visual_sentiment(file_content: bytes) -> SentimentScore:
    np_arr = np.frombuffer(file_content, np.uint8)
    cap = cv2.VideoCapture(cv2.imdecode(np_arr, cv2.IMREAD_COLOR))
    try:
        ret, frame = cap.read()
        if not ret:
            return SentimentScore(sentiment=SentimentType.NEUTRAL, confidence=0.5)
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        emotion_map = {
            "happy": SentimentType.POSITIVE,
            "sad": SentimentType.NEGATIVE,
            "angry": SentimentType.NEGATIVE,
            "neutral": SentimentType.NEUTRAL,
            "disgust": SentimentType.NEGATIVE,
            "fear": SentimentType.NEGATIVE,
            "surprise": SentimentType.NEUTRAL,
        }
        sentiment = emotion_map.get(emotion.lower(), SentimentType.NEUTRAL)
        confidence = round(result[0]['emotion'][emotion] / 100, 2)
        return SentimentScore(sentiment=sentiment, confidence=confidence)
    except:
        return SentimentScore(sentiment=SentimentType.NEUTRAL, confidence=0.5)

def combine_sentiments(text_sentiment, audio_sentiment, visual_sentiment) -> tuple[SentimentScore, bool]:
    sentiment_counts = {
        SentimentType.POSITIVE: 0,
        SentimentType.NEGATIVE: 0,
        SentimentType.NEUTRAL: 0
    }
    components = [
        (text_sentiment.sentiment, text_sentiment.confidence),
        (audio_sentiment.sentiment, audio_sentiment.confidence),
        (visual_sentiment.sentiment, visual_sentiment.confidence)
    ]
    for sentiment, confidence in components:
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += confidence
    unique_sentiments = sum(1 for count in sentiment_counts.values() if count > 0.7)
    is_ambivalent = unique_sentiments >= 2
    if is_ambivalent:
        return SentimentScore(sentiment=SentimentType.AMBIVALENT, confidence=0.8), True
    max_sentiment = max(sentiment_counts.items(), key=lambda x: x[1])
    confidence = round(max_sentiment[1] / sum(sentiment_counts.values()), 2)
    return SentimentScore(sentiment=max_sentiment[0], confidence=confidence), False

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_media(file: UploadFile = File(...)):
    content_type = file.content_type or ""
    if not (content_type.startswith("audio/") or content_type.startswith("video/")):
        raise HTTPException(status_code=400, detail="Only audio and video files are supported")
    file_content = await file.read()
    if len(file_content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    text_sentiment = analyze_text_sentiment(file_content)
    audio_sentiment = analyze_audio_sentiment(file_content)
    visual_sentiment = (
        analyze_visual_sentiment(file_content)
        if "video" in content_type
        else SentimentScore(sentiment=SentimentType.NEUTRAL, confidence=0.5)
    )

    combined_sentiment, is_ambivalent = combine_sentiments(
        text_sentiment, audio_sentiment, visual_sentiment
    )

    return SentimentResponse(
        text_sentiment=text_sentiment,
        audio_sentiment=audio_sentiment,
        visual_sentiment=visual_sentiment,
        combined_sentiment=combined_sentiment,
        is_ambivalent=is_ambivalent,
        details={
            "file_name": file.filename,
            "file_size": len(file_content),
            "content_type": content_type,
            "analysis_components": ["text", "audio", "visual"],
        }
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Multimodal Sentiment Analysis API"}
@app.get("/test-cors")
async def test_cors():
    return JSONResponse(content={"status": "CORS is working!"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)