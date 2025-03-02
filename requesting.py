import requests

# url = 'http://54.183.19.28:8000/upload'  # Replace with your server's IP and port
url = 'http://127.0.0.1:8000/upload'
file_path = '/mnt/c/Users/Vijay/Desktop/biohack25/sample-pdfs/sample_ehr.pdf'  # Replace with the path to your PDF file

# Open the PDF file in binary mode
with open(file_path, 'rb') as f:
    # Send a POST request with the file
    response = requests.post(url, files={'file': f})

# Print the response from the server
print(response.json())