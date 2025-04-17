# phishing_detector/model/feature_extractor.py
import re

def extract_features(url: str):
    return [
        len(url),
        url.count('.'),
        int('@' in url),
        int('-' in url),
        int('https' in url),
        int(bool(re.search(r'\d{1,3}(?:\.\d{1,3}){3}', url)))
    ]
