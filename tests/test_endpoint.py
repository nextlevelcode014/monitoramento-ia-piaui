import requests

url = "https://news.google.com/rss/search?q=Inteligência+Artificial+Piauí&hl=pt-BR"
response = requests.get(url)
print(f"Status: {response.status_code}")
print("Primeiros 200 caracteres:")
print(response.text[:200])
