import argparse
import mimetypes
import os
import json
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class File:
    def __init__(self, path, hash, type):
        self.path = path
        self.hash = hash
        self.type = type

def compute_file_hash(file_path):
    """Compute the SHA-256 hash of the specified file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def process_file(file_path):
    filetype = mimetypes.guess_type(file_path)
    file_hash = compute_file_hash(file_path)
    file_object = File(file_path, file_hash, filetype[0])
    return file_path, file_hash, filetype[0], file_object

def scan_directory(directory):
    list_of_extensions = {}
    unknown_extensions = []
    file_hashes = {}
    file_objects = {}

    with ThreadPoolExecutor() as executor:
        futures = []
        for root, dirs, files in os.walk(directory):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(process_file, file_path))

        for future in as_completed(futures):
            file_path, file_hash, filetype, file_object = future.result()
            print(file_path)

            if file_hash in file_hashes:
                print(f"Duplicate found: {file_path} is a duplicate of {file_hashes[file_hash]}")
                continue
            else:
                file_hashes[file_hash] = file_path

            if filetype is not None:
                if filetype not in file_objects:
                    file_objects[filetype] = []
                list_of_extensions[filetype] = list_of_extensions.get(filetype, 0) + 1
                file_objects[filetype].append(file_object)
            else:
                if 'unknown' not in file_objects:
                    file_objects['unknown'] = []
                unknown_extensions.append(file_path)
                file_objects['unknown'].append(file_object)
        list_of_extensions['unknown'] = unknown_extensions
    return (list_of_extensions, file_objects)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Tool to organize a file system based on file extension")
    parser.add_argument('-d', '--directory', help="Directory to scan")
    parser.add_argument('-o', '--output', help="Output directory to write the results to")
    args = parser.parse_args()

    time_start = time.time()
    mimetypes.init()
    mime_types = mimetypes.types_map
        
    if args.directory:
        directory = args.directory
    else:
        directory = os.getcwd()

    list_of_extensions, files = scan_directory(directory)

    # write list_of_extensions to a file
    if os.path.exists('file_extensions.txt'):
        os.remove('file_extensions.txt')
    with open('file_types.txt', 'w') as f:
        f.write('Different Extensions Found: %d\n\n' % len(list_of_extensions))
        for item in list_of_extensions:
            if item == "unknown":
                f.write('Unknown Extensions:\n')
                for unknown in list_of_extensions[item]:
                    f.write('\t%s\n' % unknown)
            else:
                f.write("%s : %d\n" % (item, list_of_extensions[item]))
    
    # design the output directory structure
    if os.path.isfile('file_objects.json'):
        os.remove('file_objects.json')
    json.dump(files, open('file_objects.json', 'w'), default=lambda x: x.__dict__)

    print(list_of_extensions)
    time_end = time.time()
    print(f"Time taken: {time_end - time_start} seconds")
