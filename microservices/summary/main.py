import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

from fastapi import FastAPI
from pydantic import BaseModel
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter

app = FastAPI()

@app.get("/")
def hcheck():
    return {"status": "summary service running successfully"}

class TextInput(BaseModel):
    text: str
    max_sentences: int = 3


def summarize_text(text: str, max_sentences: int):
    # 1. Sentence tokenize
    sentences = sent_tokenize(text)

    # Safety check
    if max_sentences >= len(sentences):
        return text

    # 2. Word tokenize + clean
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))

    filtered_words = [
        word for word in words
        if word.isalnum() and word not in stop_words
    ]

    # 3. Word frequency
    word_frequencies = Counter(filtered_words)

    # 4. Sentence scoring (WITH position bias)
    sentence_scores = {}

    for idx, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

        # 🔥 Position bias (earlier sentences boosted)
        sentence_scores[sentence] += (len(sentences) - idx) * 0.5

    # 5. Pick top N sentences
    ranked_sentences = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:max_sentences]

    # 6. Preserve original order
    summary = [
        sentence for sentence in sentences
        if sentence in ranked_sentences
    ]

    return " ".join(summary)


@app.post("/summarize")
def summarize(input: TextInput):
    summary = summarize_text(input.text, input.max_sentences)

    return {
        "summary": summary,
        "sentences_requested": input.max_sentences
    }
