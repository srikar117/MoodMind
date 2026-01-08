from fastapi import FastAPI
from pydantic import BaseModel #used to define structure of json
from textblob import TextBlob  #nlp sentiment analyzer

app = FastAPI()

@app.get("/")                  #just a health check route
def health():
    return{'status' : 'sentiment service running successfully'}

class TextInput(BaseModel):  #created a data model called TextInput
    text : str               #the incoming json structure, data validation

@app.post("/sentiment")      #it tells the app to run below function
def analyze_sentiment(input : TextInput):
    blob = TextBlob(input.text)
    polarity = blob.sentiment.polarity

    if polarity > 0:          #labelling of sentiment
        label = "Positive"
    elif polarity < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return {
        "text" : input.text,  #send this json back to client
        'sentiment' : label,
        'score' : polarity
    }