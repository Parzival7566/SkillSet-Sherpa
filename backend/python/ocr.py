import requests
import re

# Specify the URL of the PDF data extraction API
url = "https://api.worqhat.com/api/ai/v2/pdf-extract"

# Specify the path to the PDF file you want to extract data from
pdf_file_path = "/content/Class X Original Marksheet.pdf"

# Create a dictionary to hold the PDF file data
files = {'file': (pdf_file_path, open(pdf_file_path, 'rb'))}

# Specify your API token in the 'Authorization' header
headers = {
    "Authorization": "Bearer sk-c9d067cb72fc47af953e9dfc8d26b9da"
}

# Send a POST request to the API with the PDF data
response = requests.post(url, files=files, headers=headers)

# Check the response from the API
if response.status_code == 200:
    content = response.json().get("content", "No content available.")
    
    # Extract only the content part
    content_start = content.find("MARKS STATEMENT CUM CERTIFICATE")
    if content_start != -1:
        content = content[content_start:]

    # Clean up the content by removing extra spaces and formatting
    content = re.sub(r'\n{2,}', '\n', content)  # Remove consecutive line breaks
    #content = content.replace('|', '')  # Remove pipe characters
    content = content.replace(' :', ':')  # Remove spaces before colons

    # Print the formatted content
    print(content)

    # Export the result to a text file
    with open("prompt.txt", "w") as output_file:
        output_file.write(content)

    print("Result exported to 'prompt.txt'")
else:
    print("Error:", response.text)
