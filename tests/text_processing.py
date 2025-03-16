import requests

url = "http://127.0.0.1:8000/process_text"
file_path = "sample.txt"  # Make sure this file exists

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

# Extract chunks from the response
data = response.json()
print("Full Response:", data)

# Print chunks separately
if "chunks" in data:
    print("\nChunks:")
    for i, chunk in enumerate(data["chunks"], 1):
        print(f"Chunk {i}: {chunk}")
else:
    print("No chunks found in response.")
