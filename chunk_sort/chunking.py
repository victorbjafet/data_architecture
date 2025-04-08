import os.path
import sys

def get_chunk_indices(filename, relative_chunk_number, chunk_size, start_index):
    #print(relative_chunk_number, chunk_size, start_index)
    try:
        with open(filename, 'rb') as file:
            #the point of having a start index is to optimize finding chunks, preventing needing to calculate every chunk from start to end of file each time if you already calculated a certain amount and know their end index
            bindex = start_index #starting index of the chunk calculation, 0 for beginning of file. cursor should be before first byte of chunk
            findex = start_index #where the index of the chunk start will be stored
            for i in range(relative_chunk_number): #calculate where each chunk ends one at a time
                #print("Chunk " + str(i + 1))
                bindex += chunk_size - 1 #right before the last byte of the chunk
                file.seek(bindex) #puts the cursor there 
                offset = 0 #how many bytes behind the end of the theoretical chunk the newline is
                chunk_data = file.read(1) #read last byte of chunk
                while chunk_data != b'\n': #checks if the last read byte is a newline
                    if chunk_data == b'':
                        raise Exception("Reached end of file")
                    file.seek(-2, 1) #puts the cursor back 2 bytes
                    offset -= 1 #changes offset accordingly
                    #print("Char: " + str(chunk_data))
                    #print("Offset: " + str(offset))
                    chunk_data = file.read(1) #reads one byte moving the cursor up a byte (net movement one byte)
                bindex += offset #adjusts the current index based on calculated offset
                #print("Current index: " + str(bindex))
                if i == relative_chunk_number - 2:
                    findex = bindex + 1
        #print(findex, bindex)
        #print("Index discovery done")
        return (findex, bindex) #inclusive, non inclusive (index of first byte in chunk, index of newline after last byte in chunk) 
    except Exception as e:
        print("Error calculating chunk start index", e)
        raise Exception(str(e))


def get_chunk(filename, relative_chunk_number, chunk_size, start_index):
    try:
        findex, bindex = get_chunk_indices(filename, relative_chunk_number, chunk_size, start_index)
    except Exception as e:
        raise Exception("Failed get_chunk_indices in get_chunk: get_chunk_indices(" + filename + ", " + str(relative_chunk_number) + ", " + str(chunk_size) + ", " + str(start_index) + ") returns error " + str(e) + " | Check that NFS is working on dispy nodes")
    #print(findex, bindex) 
    try:
        with open(filename, 'r') as file:
            file.seek(findex)
            chunk_str = file.read(bindex-findex)
            #print(chunk_str)
            ints_list = chunk_str.strip().split("\n")
            #print(ints_list)
            for i in range(len(ints_list)):
               ints_list[i] = int(ints_list[i].strip())
            #print(ints_list)
            return bindex, ints_list
    except Exception as e:
        print("Error reading chunk", e)     






            
#filename = "/home/orangepi/nfsshare/data1.set"
#
#try:
#    chunk_number = int(input("Chunk number: "))
#except ValueError:
#    print("Error: chunk_number \"{}\" is not an integer".format(sys.argv[2]))
#    exit(1)
#
#try:
#    chunk_size = int(input("Chunk size: "))
#except ValueError:
#    print("Error: chunk_size \"{}\" is not an integer".format(sys.argv[3]))
#    exit(1)
#
#if chunk_size < 20:
#    print("Error: chunk_size must be >= 20")
#    exit(1)
#
#
#
#output = "chunk_test.txt"
#
#
#
#end_index = -1
#
#for i in range(chunk_number):
#    print(get_chunk_indices(filename, i + 1, chunk_size, 0))
#    if i == 0:
#        with open(output, 'w') as file:
#            pass
#    with open(output, 'a') as file:
#        end_index, int_array = get_chunk(filename, 1, chunk_size, end_index + 1) #end index + 1 because that is the position for the cursor to be before the first byte of the next chunk
#        print(int_array)
#        print()
#        for num in int_array:
#            file.write(str(num) + "\n")
#
