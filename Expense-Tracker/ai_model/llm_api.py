import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama3",
    "prompt": "3 Latest CASIO analog automatic watches released in 2025 for men"
}
response = requests.post(url, json=payload, stream=True)
for line in response.iter_lines():
    if line:
        decode_line=line.decode("utf-8")
        json_object=json.loads(decode_line)
        actual_text = json_object.get("response","")
        print(actual_text,end="")