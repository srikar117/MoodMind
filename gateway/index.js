const express = require('express')
const axios = require('axios')
const cors = require('cors')
const multer = require('multer')

const app = express()
const upload = multer()

app.use(cors())
app.use(express.json())
