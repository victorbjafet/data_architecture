import os.path
import sys

def get_chunk_start_index(filename, chunk_number, chunk_size):
    try:
        with open(filename, 'rb') as file:
            bindex = 0 #starting index of the file, cursor is before first byte
            findex = 0 #where the index of the chunk start will be stored
            for i in range(chunk_number): #calculate where each chunk ends one at a time
                print("Chunk " + str(i))
                bindex += chunk_size - 1 #right before the last byte of the chunk
                file.seek(bindex) #puts the cursor there 
                offset = 0 #how many bytes behind the end of the theoretical chunk the newline is
                chunk_data = file.read(1) #read last byte of chunk
                while chunk_data != b'\n': #checks if the last read byte is a newline
                    file.seek(-2, 1) #puts the cursor back 2 bytes
                    offset -= 1 #changes offset accordingly
                    print("Char: " + str(chunk_data))
                    print("Offset: " + str(offset))
                    chunk_data = file.read(1) #reads one byte moving the cursor up a byte (net movement one byte)
                bindex += offset #adjusts the current index based on calculated offset
                print("Current index: " + str(bindex))
                if i == chunk_number - 2:
                    findex = bindex
        print(findex, bindex)
        print("Index discovery done")
        return (findex, bindex) 
    except Exception as e:
        print("Error calculating chunk start index", e)


def get_chunk(filename, chunk_number, chunk_size):
    sindex, eindex = get_chunk_start_index(filename, chunk_number, chunk_size) 
#    try:
    with open(filename, 'r') as file:
        file.seek(sindex)
        chunk_str = file.read(eindex-sindex)
        print(chunk_str)
        ints_list = chunk_str.strip().split("\n")
        print(ints_list)
        for i in range(len(ints_list)):
           ints_list[i] = int(ints_list[i].strip())
        print(ints_list)
        return ints_list
#    except Exception as e:
#        pass
#        print("Error reading chunk", e)     






            
filename = "/home/orangepi/nfsshare/data1.set"

if not os.path.exists(filename):
    print("File \"{}\" does not exist".format(filename))
    exit(1)

try:
    chunk_number = int(input("Chunk number: "))
except ValueError:
    print("Error: chunk_number \"{}\" is not an integer".format(sys.argv[2]))
    exit(1)

try:
    chunk_size = int(input("Chunk size: "))
except ValueError:
    print("Error: chunk_size \"{}\" is not an integer".format(sys.argv[3]))
    exit(1)

if chunk_size < 20:
    print("Error: chunk_size must be > 20")
    exit(1)



output = "chunk_test.txt"

for i in range(chunk_number):
    if i == 0:
        with open(output, 'w') as file:
            pass
    with open(output, 'a') as file:
        int_array = get_chunk(filename, i + 1, chunk_size)
        for num in int_array:
            file.write(str(num) + "\n")

