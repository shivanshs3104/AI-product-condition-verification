# TrustLens AI

AI-based product condition verification system with Flask backend and React frontend.

## Overview
TrustLens AI analyzes product images to detect visible damage and estimate a fair resale price.

## Features
- Image upload and validation
- Damage detection using YOLO pipeline
- Severity scoring and explanation
- Recommended resale price
- Duplicate image detection using hash

## Tech Stack
- Frontend: React + Vite
- Backend: Python + Flask
- AI/ML: YOLOv8, OpenCV, PyTorch
- Database: SQLite

## Project Structure
```
Ai-Collaborator_Project/
	backend/
		app.py
		db.py
		damage_detector_yolo.py
		image_utils.py
		utils/
	frontend/
		src/
		package.json
		vite.config.js
	docs/
	README.md
```

## Local Development

### 1) Run Backend
```
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs on `http://127.0.0.1:5000`.

### 2) Run Frontend (Dev Mode)
```
cd frontend
npm install
npm run dev
```
Frontend runs on `http://127.0.0.1:5173` and uses Vite proxy for API calls.

## Production-like Run (Flask serves React build)
1. Build frontend:
```
cd frontend
npm install
npm run build
```
2. Start backend:
```
cd backend
python app.py
```
3. Open app at `http://127.0.0.1:5000/app`.

## Main API Endpoints
- `GET /health`
- `POST /upload-image`
- `GET /products`

## Notes
- Frontend build folder (`frontend/dist`) is required for `/app` route.
- Upload endpoint expects multipart form-data with key: `image`.

