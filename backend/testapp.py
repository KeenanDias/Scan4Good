import google.generativeai as genai
import os

# PASTE YOUR REAL KEY HERE
GEMINI_API_KEY = "AIzaSyAwUkVRg3EMlMA1g81e3UzgIP0dVw48tH0" 
genai.configure(api_key=GEMINI_API_KEY)

print(f"📚 Library Version: {genai.__version__}")
print("🔍 Checking available models for your key...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
            
    # Try a quick test generation
    print("\n🤖 Testing connection with 'gemini-1.5-flash'...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hello, are you working?")
    print(f"💬 RESPONSE: {response.text}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")