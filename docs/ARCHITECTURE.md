# TrustLens AI Architecture

## Overview
TrustLens AI is an AI-based system that analyzes the condition of products using computer vision and suggests a fair resale price.

## System Components

### Frontend
Handles user interaction.

Technologies:
- React.js
- HTML
- CSS
- JavaScript

Functions:
- Upload product images
- Display analysis results
- Show recommended price

### Backend
Handles processing and API requests.

Technologies:
- Python
- Flask

Functions:
- Receive uploaded images
- Generate image hash
- Detect duplicates
- Call AI damage detection module
- Store results in database

### AI Model
Detects damage in product images.

Technologies:
- YOLOv8
- OpenCV
- PyTorch

Functions:
- Detect damage
- Calculate severity score
- Generate explanation

### Pricing Engine
Calculates recommended price based on damage severity.

### Database
Stores product analysis results.

Technology:
- SQLite