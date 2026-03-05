# TrustLens AI

AI-Based Product Condition Verification System

## Overview
TrustLens AI analyzes product images to detect damage and recommend a fair resale price.

## Features
- Image upload
- Damage detection
- Severity scoring
- Price recommendation
- Duplicate image detection

## Tech Stack

Frontend
- React.js
- HTML
- CSS

Backend
- Python
- Flask

AI / Machine Learning
- YOLOv8
- OpenCV
- PyTorch

Database
- SQLite

## Project Structure

trustlens-ai
│
├── backend
│   ├── app.py
│   ├── db.py
│   ├── damage_detector_yolo.py
│   └── utils
│
├── frontend
│
├── docs
│   └── ARCHITECTURE.md
│
└── README.md

## Running the Project

Install dependencies:

pip install -r requirements.txt

Run backend:

python app.py