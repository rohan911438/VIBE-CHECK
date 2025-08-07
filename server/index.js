const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const DATA_FILE = path.join(__dirname, 'quiz_results.json');

app.use(cors());
app.use(express.json());

// Helper: Read/Write JSON file
function readResults() {
    if (!fs.existsSync(DATA_FILE)) return [];
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf-8'));
}
function writeResults(data) {
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

// API: Get all quiz results
app.get('/api/results', (req, res) => {
    res.json(readResults());
});

// API: Add a new quiz result
app.post('/api/results', (req, res) => {
    const { name, date, score } = req.body;
    if (!name || !date || typeof score !== 'number') {
        return res.status(400).json({ error: 'Invalid data' });
    }
    const results = readResults();
    results.push({ name, date, score });
    writeResults(results);
    res.status(201).json({ message: 'Result saved' });
});

// Remove app.listen() and export the app object for Vercel
module.exports = app;
