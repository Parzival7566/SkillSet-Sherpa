import requests

url = "https://api.worqhat.com/api/ai/content/v3"

headers = {
    "Authorization": "Bearer sk-c9d067cb72fc47af953e9dfc8d26b9da",
    "Content-Type": "application/json"
}

# Read the question from a text file
with open("question.txt", "r") as question_file:
    question = question_file.read()

data = {
    "question": question,
    "randomness": 0.4
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    content = response.json().get("content")

    content = content.replace("\n\n", "\n")

    print(content)
else:
    print("Error:", response.text)
