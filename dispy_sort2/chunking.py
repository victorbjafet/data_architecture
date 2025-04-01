import os.path
import sys

def get_chunk(filename, chunk_number, chunk_size):
    try:
        with open(filename, 'r') as file:
            file.seek(chunk_size * chunk_number)
            chunk_data = file.read(chunk_size)

            lines = chunk_data.split('\n')
            if chunk_data and file.tell() != os.fstat(file.fileno()).st_size:
                last_line = lines.pop() #removes end number
                file.seek(file.tell() - len(last_line))
            
            for line in lines:
                if line.strip().isdigit():
                    print(line.strip())
    except Exception as e:
        print("Error reading chunk:", e)

args = sys.argv[1:]

if len(args) != 3:
    print("Usage: python {} <filename> <chunk_number> <chunk_size_in_bytes>".format(sys.argv[0]))
    exit(1)

filename = sys.argv[1]

if not os.path.exists(filename):
    print("File \"{}\" does not exist".format(filename))
    exit(1)

try:
    chunk_number = int(sys.argv[2])
except ValueError:
    print("Error: chunk_number \"{}\" is not an integer".format(sys.argv[2]))
    exit(1)

try:
    chunk_size = int(sys.argv[3])
except ValueError:
    print("Error: chunk_size \"{}\" is not an integer".format(sys.argv[3]))
    exit(1)

if chunk_size < 10:
    print("Error: chunk_size must be > 10")
    exit(1)

get_chunk(filename, chunk_number, chunk_size)
