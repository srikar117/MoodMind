import streamlit as st
import requests

GATEWAY_URL = "http://localhost:3000"

st.set_page_config(                                #page config
    page_title = "MoodMind Microservices",
    layout = 'centered'
)

st.title("MoodMind Microservices")
st.write("Sentiment Analysis    Text Summarizaton   Image Tagging")

st.divider()

st.subheader("Sentiment Analysis")                 #sentiment text field
sentiment_text = st.text_area(
    "Enter text for sentiment analysis",
    placeholder = "I love building ML and backend systems"
)
if st.button("Analyze Sentiment"):
    if sentiment_text.strip() == " ":
        st.warning("Please enter some text.")
    else:
        response = requests.post(
            f"{GATEWAY_URL}/api/sentiment",
            json = {"text" : sentiment_text}
        )
        st.json(response.json())

st.divider()

st.subheader("Text Summarization")                 #summary text field
summary_text = st.text_area(
    "Enter text to summarize",
    placeholder = "Paste a paragraph or long article."
)
max_sentences = st.slider(
    "Max Sentences",
    min_value = 1,
    max_value = 5,
    value = 2
)
if st.button("Summarize Text"):
    if summary_text.strip() == " ":
        st.warning("Please enter some text.")
    else:
        response = requests.post(
            f"{GATEWAY_URL}/api/summary",
            json = {
                "text" : summary_text,
                "max_sentences" : max_sentences
            }
        )
        st.json(response.json())

st.divider()

st.subheader("Image Tagging")
uploaded_image = st.file_uploader(
    "Upload an Image",
    type = ['jpg', 'jpeg', 'png']
)
if st.button("Tag Image"):
    if uploaded_image is None:
        st.warning("Please upload a valid image.")
    else:
        files = {
            "image" : uploaded_image.getvalue()
        }
        response = requests.post(
            f"{GATEWAY_URL}/api/image-tags",
            files = files
        )
        st.image(uploaded_image, caption = "Uploaded Image", width = 
        st.json(response.json)