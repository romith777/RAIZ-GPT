const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = 5000;
const PYTHON_API_URL = 'http://localhost:5001/chat';

app.use(cors());
app.use(express.json());

// Main chat endpoint that proxies to Python microservice
app.post('/api/chat', async (req, res) => {
    try {
        const { instruction, input } = req.body;
        
        if (!instruction) {
            return res.status(400).json({ error: 'Instruction is required' });
        }

        // Send request to Python Flask model API
        const response = await axios.post(PYTHON_API_URL, {
            instruction,
            input: input || ''
        });

        // Return the response back to React frontend
        res.json({ response: response.data.response });
    } catch (error) {
        console.error('Error communicating with model API:', error.message);
        res.status(500).json({ 
            error: 'Failed to communicate with the model backend. Make sure the Python microservice is running.' 
        });
    }
});

app.listen(PORT, () => {
    console.log(`Node.js backend is running on http://localhost:${PORT}`);
});
