from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import logging
from urllib.parse import urlparse
from model.feature_extractor import extract_features

# Initialize the FastAPI app and load the trained model
app = FastAPI()
model = joblib.load("model/phishing_model.pkl")

# Set up logging to monitor the usage
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Input data schema using Pydantic
class URLRequest(BaseModel):
    url: str

# Function to check if a URL is valid
def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

# Root endpoint for basic health check
@app.get("/")
def root():
    return {"status": "Phishing Detector API is running 🚀"}

# Prediction endpoint
@app.post("/predict")
def predict_url(data: URLRequest):
    # Validate the URL format
    if not is_valid_url(data.url):
        logging.error(f"Invalid URL format: {data.url}")
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    try:
        # Extract features from the URL
        features = extract_features(data.url)
        
        # Make a prediction
        prediction = model.predict([features])[0]
        
        # Determine the result based on the prediction (1 = legitimate, 0 = phishing)
        result = "legitimate" if prediction == 1 else "phishing"
        
        # Log the URL and its prediction for monitoring
        logging.info(f"URL: {data.url} | Prediction: {result}")
        
        # Return the prediction result
        return {"prediction": result}

    except Exception as e:
        # Log the exception error and raise HTTP exception
        logging.error(f"Error processing the URL: {data.url} | Error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the URL")
