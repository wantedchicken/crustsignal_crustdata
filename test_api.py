import requests
import os
from dotenv import load_dotenv

load_dotenv()

CRUSTDATA_API_KEY = os.getenv("CRUSTDATA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Test 1: Check keys loaded
print("=== Checking API Keys ===")
print(f"Crustdata Key: {'✅ Loaded' if CRUSTDATA_API_KEY else '❌ Missing'}")
print(f"OpenAI Key: {'✅ Loaded' if OPENAI_API_KEY else '❌ Missing'}")

# Test 2: Test Crustdata API
print("\n=== Testing Crustdata API ===")
headers = {
    "Authorization": f"Token {CRUSTDATA_API_KEY}",
    "Accept": "application/json"
}

response = requests.get(
    "https://api.crustdata.com/screener/company",
    headers=headers,
    params={
        "company_domain": "openai.com",
        "fields": "job_openings"
    }
)

print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print("✅ Crustdata API working!")
    data = response.json()
    print(f"Sample response: {data[0] if data else 'Empty'}")
else:
    print(f"❌ Error: {response.text}")

# Test 3: Test OpenAI API
print("\n=== Testing OpenAI API ===")
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hello in one word"}]
    )
    print(f"✅ OpenAI API working!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")