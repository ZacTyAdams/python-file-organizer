import argparse
import mimetypes
import os
import json
import mimetypes

def gather_file_types(directory):
    global extensions
    list_of_extensions = {}
    unknown_extensions = []

    for root, dirs, files in os.walk(directory):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for file in files:
            file_path = os.path.join(root, file)
            print(file_path)
            filetype = mimetypes.guess_type(file_path)
            if filetype[0] is not None:
                list_of_extensions[filetype[0]] = list_of_extensions.get(filetype[0], 0) + 1
            else:
                unknown_extensions.append(file_path)
        list_of_extensions['unknown'] = unknown_extensions
    return list_of_extensions

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Tool to organize a file system based on file extension")
    parser.add_argument('-d', '--directory', help="Directory to scan")
    args = parser.parse_args()

    mimetypes.init()
    mime_types = mimetypes.types_map
        
    if args.directory:
        directory = args.directory
    else:
        directory = os.getcwd()

    list_of_extensions = gather_file_types(directory)
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

    print(list_of_extensions)
