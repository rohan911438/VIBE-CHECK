# Vibe Check Backend

This is a simple Express.js backend for the Vibe Check project. It provides REST API endpoints to store and retrieve quiz results.

## Features
- Store quiz results (name, date, score) in a JSON file
- Retrieve all quiz results
- CORS enabled for frontend integration

## Usage

1. Install dependencies:
   ```bash
   cd server
   npm install
   ```
2. Start the server:
   ```bash
   npm start
   ```
   The backend will run on http://localhost:3001

## API Endpoints
- `GET /api/results` — Get all quiz results
- `POST /api/results` — Add a new quiz result (JSON: `{ name, date, score }`)

## Note
- This backend uses a local JSON file for storage. For production, use a real database (MongoDB, PostgreSQL, etc).
