if __name__ == "__main__":
    
    #filename = input("Enter the file to read (empty for default): ")
    #if not filename: 
    filename = '/home/orangepi/nfsshare/datasets/data1.set'
    filenamesolo = filename[filename.rindex("/") + 1:]
    
    try:
        n = int(input("Enter the number of bytes to read: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the count.")
    
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
    print("Done")
