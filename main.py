import argparse
import os

def gather_file_types(directory):
    list_of_extensions = []
    for root, dirs, files in os.walk(directory):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for file in files:
            extension = file.split('.')[-1]
            print(file)
            print(root)
            if extension not in list_of_extensions:
                list_of_extensions.append(extension)
    return list_of_extensions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to organize a file system based on file extension")
    parser.add_argument('-d', '--directory', help="Directory to scan")
    args = parser.parse_args()

    if args.directory:
        directory = args.directory
    else:
        directory = os.getcwd()

    list_of_extensions = gather_file_types(directory)
    # write list_of_extensions to a file
    with open('file_types.txt', 'w') as f:
        for item in list_of_extensions:
            f.write("%s\n" % item)
            
    print(list_of_extensions)
