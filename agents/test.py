from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

my_file = client.files.upload(file="/home/laky/Desktop/hackathon/medicai/agents/coke.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[my_file, "Caption this image."],
    
)

print(response.text)