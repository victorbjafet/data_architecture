if __name__ == "__main__":
    import sys
    sys.path.append("/home/orangepi/nfsshare/chunk_sort/")
    from chunking import get_chunk_indices    
    #filename = input("Enter the file to read (empty for default): ")
    #if not filename: 
    filename = '/home/orangepi/nfsshare/datasets/data1.set'
    filenamesolo = filename[filename.rindex("/") + 1:]
    
    try:
        chunk_number = int(input("Enter the number of chunks: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the count.")
    
    try:
        chunk_size = int(input("Enter the size of each chunk: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the count.")

    n = get_chunk_indices(filename, chunk_number, chunk_size, 0)[1]


    integers = ""
    with open(filename, 'r') as file:
        for i in range(n):
            integers += file.read(1)
    integers = integers.split("\n")
    integers2 = []
    for numb in integers:
       integers2.append(int(numb)) 
    sorted_numbers = sorted(integers2)

    with open("/home/orangepi/nfsshare/outputs/" + filenamesolo + "_validate_" + str(n) + "b.txt", 'w') as file:
        for number in sorted_numbers:
            file.write(f"{number}\n")
    print("Done, " + str(n) + " bytes sorted")
