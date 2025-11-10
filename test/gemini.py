from google import genai

client = genai.Client(api_key="AIzaSyBhXKElTaYia86NDD3TqXmO1p158QwAfnw")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Qui est Madick Ange César?"
)
print(response.text)