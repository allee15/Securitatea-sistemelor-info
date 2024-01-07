import os
import hashlib


# Function to extract header from a PPM file
def extract_header(file_path):
    with open(file_path, 'rb') as file:
        header = b''
        while True:
            line = file.readline()
            header += line
            if line.strip() == b'255':
                break
        return header.decode('ascii')


def hash_headers(header):
    return hashlib.sha256(header.encode('utf-8')).hexdigest()


# Directory containing your PPM files
ppm_files_directory = 'my_name'

headers = []
headers_hashed = []
# Extract headers from each PPM file in the directory
for filename in os.listdir(ppm_files_directory):
    file_path = os.path.join(ppm_files_directory, filename)
    header = extract_header(file_path)
    headers.append(header)
    headers_hashed.append(hash_headers(header))

# Print extracted headers
for idx, header in enumerate(headers, start=1):
    hashed_header = hash_headers(header)
    headers_hashed.append(hashed_header)
    print(f"Header {idx}: {header}\n Hash: {hashed_header}")
