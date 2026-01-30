const express = require('express')
const axios = require('axios')
const cors = require('cors')
const multer = require('multer')
const FormData = require('form-data')

const app = express()
const upload = multer()

app.use(cors())
app.use(express.json())

const SERVICES = {
    sentiment : "http://localhost:8001/sentiment",
    summarize : "http://localhost:8002/summarize",
    image : "http://localhost:8003/tag-image"
};

app.post("/api/sentiment", async (req,res) => {
    try{
        const response = await axios.post(
            SERVICES.sentiment,
            req.body
        )
        res.json(response.data)
    } catch (error) {
        console.error("Sentiment Error:", error.message)
        res.status(500).json({error : "Sentiment service failed"})
    }
})

app.post("/api/summary", async (req,res) => {
    try{
        const response = await axios.post(
            SERVICES.summarize,
            req.body
        )
        res.json(response.data)
    } catch (error) {
        console.error("Summary Error:", error.message)
        res.status(500).json({error : "Summary service failed"})
    }
})

app.post(
    '/api/image-tags',
    upload.single('image'),
    async (req,res) => {
        try{
            const formData = new FormData()
            formData.append(
                'image',
                req.file.buffer,
                req.file.originalname
            )

            const response = await axios.post(
                SERVICES.image,
                formData,
                {
                    headers : formData.getHeaders()
                }
            )
            res.json(response.data)
        } catch (error) {
            res.status(500).json({error : 'Image tagging service failed'})
        }
    }
)

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`API Gateway running on port ${PORT}`)
});