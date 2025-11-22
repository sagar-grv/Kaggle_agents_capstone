
import google.generativeai as genai
import os

key = "AIzaSyBR0fPdqCAB7_6ASAj8cK-T4atrkfHz6TU"
os.environ["GOOGLE_API_KEY"] = key
genai.configure(api_key=key)

try:
    model = genai.GenerativeModel('gemini-flash-latest')
    response = model.generate_content("Hello, are you working?")
    print(f"Success! Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
