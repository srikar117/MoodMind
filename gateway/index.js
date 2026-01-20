const express = require('express')
const axios = require('axios')
const cors = require('cors')
const multer = require('multer')

const app = express()
const upload = multer()

app.use(cors())
app.use(express.json())

const SERVICES = {
    sentiment : "http://localhost:8001/sentiment",
    summarize : "http://localhost:8002/summarize",
    image : "http://localhost:8003/tag-image"
};

