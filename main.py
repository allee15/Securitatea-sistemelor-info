
import hashlib
import os
import shutil

# Static array of hash values
hash_values = [
    '602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d',
    'f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5',
    'aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5',
    '70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450',
    '77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6',
    '456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01',
    'bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d',
    '372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305'
]


def generate_header(x, y):
    return f'P6 {x} {y} 255'


def alternative(x, y):
    return f'P6\n{x} {y}\n255\n'


z = 1
# Brute force to find matching hash
for x in range(1, 1001):
    for y in range(1, 1001):
        header = generate_header(x, y)
        formatted_header = alternative(x, y)
        hash_val = hashlib.sha256(header.encode()).hexdigest()
        if hash_val in hash_values:
            print(f"Match found for hash value {hash_val} with header: {header}")

            # Create duplicate files with header
            src_folder = 'encrypted_files'
            dest_folder = f'duplicates_with_header{z}'
            z += 1

            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            # Read files from encrypted_files folder and create duplicates with headers
            for filename in os.listdir(src_folder):
                src_file_path = os.path.join(src_folder, filename)
                dest_file_path = os.path.join(dest_folder, filename)
                with open(src_file_path, 'rb') as src_file:
                    with open(dest_file_path, 'wb') as dest_file:
                        new_file_content = formatted_header.encode('ascii') + src_file.read()
                        dest_file.write(new_file_content)

            print("Duplicate files with headers created in 'duplicates_with_header' folder.")
            break
