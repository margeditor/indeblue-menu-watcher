import requests

url = "https://www.instagram.com/indeblueindianbistro/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}

r = requests.get(url, headers=headers)

print("Status:", r.status_code)
print("Length:", len(r.text))

for term in ["buffet", "Paneer", "Butter", "Lunch"]:
    print(term, term.lower() in r.text.lower())

print(r.text[:500])
