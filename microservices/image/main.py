from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch

app = FastAPI()

@app.get('/')
def healthcheck():
    return {'status' : 'image tagging service running successfully'}

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

CANDIDATE_LABELS = [
    'person', 'dog', 'cat', 'car', 'food',
    'nature', 'building', 'technology',
    'animal', 'outdoor', 'indoor'
]

@app.post("/tag-image")
def tag_image(file : UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file. Please upload a valid image.")

    inputs = processor(
        text = CANDIDATE_LABELS,
        images = image,
        return_tensors = "pt",
        padding = True
    )

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image    #contains raw similarity score between image and each text label
    probs = logits_per_image.softmax(dim = 1)      #converts the raw scores btw 0 and 1, that sum upto 1

    top_results = probs[0].topk(5)

    threshold = 0.20

    tags = []
    for idx, score in zip(top_results.indices.tolist(), top_results.values.tolist()):
        if score >= threshold:
            tags.append(CANDIDATE_LABELS[idx])

    return {
        'tags' : tags
    }