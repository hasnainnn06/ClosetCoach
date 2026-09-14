import requests
import json

# Test CIR endpoint with image file
print("Testing CIR endpoint with image...")

# Use an existing temp image file
image_path = "temp_upload.jpg"  # This file exists in the project

with open(image_path, "rb") as f:
    files = {"image": ("test_image.jpg", f, "image/jpeg")}
    data = {
        "gender": "female",
        "category": "top",
        "mood": "casual",
        "occasion": "daily",
        "weather": "moderate"
    }
    
    response = requests.post(
        'http://127.0.0.1:5050/api/cir',
        files=files,
        data=data
    )

print(f"Status Code: {response.status_code}")
try:
    result = response.json()
    # Don't print base64 images (too long)
    if result.get("success") and result.get("matches"):
        print("SUCCESS! CIR Results:")
        for match in result["matches"]:
            print(f"  - {match['category']}: score={match['score']}")
        print(f"Reasoning: {result.get('reasoning', [])}")
    else:
        print(f"Response: {json.dumps(result, indent=2)}")
except Exception as e:
    print(f"Error parsing response: {e}")
    print(f"Raw response: {response.text[:500]}")
