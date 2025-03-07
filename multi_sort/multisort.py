import multiprocessing
import time

def read_and_split(file_path, readcount, splitcount):
    with open(file_path, 'r') as file:
        numbers = [int(line.strip()) for _, line in zip(range(readcount), file)]

    chunk_size = len(numbers) // splitcount
    remainder = len(numbers) % splitcount

    result = []
    index = 0
    for i in range(splitcount):
        extra = 1 if i < remainder else 0  # distribute remainder
        result.append(numbers[index:index + chunk_size + extra])
        index += chunk_size + extra
    
    return result



def worker(input_queue, output_queue):
    while True:
        numbers = input_queue.get()

        if numbers == None:
            print(multiprocessing.current_process().name + " killed")
            break #stop worker if no more to sort

        start_time = time.time()

        n = len(numbers)
        print(multiprocessing.current_process().name + " started sorting " + str(n) + " numbers @ " + str(start_time))
        
        counter = 0
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if numbers[j] > numbers[j + 1]:
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                    swapped = True
            if not swapped:
                break
            if counter == n//4: #change this number to change print frequency
                print(multiprocessing.current_process().name + " | " +str(time.time() - start_time) + "s | " + str(i) + " sorted")
                counter = 0
            counter += 1
        
        print(multiprocessing.current_process().name + " finished sorting " + str(n) + " numbers @ " + str(time.time() - start_time))
        output_queue.put(numbers)





if __name__ == "__main__":
    #input_file = "data1.set"
    #output_file = "output.txt"

    input_file = "/home/orangepi/nfsshare/data1.set"
    output_file = "/home/orangepi/nfsshare/output.txt"

    try:
        n = int(input("Number of ints to sort: "))
    except:
        print("Not an integer")
        raise ValueError
    
    with open(input_file, 'r') as file:
        count = [int(line.strip()) for _, line in zip(range(n), file)]

    if len(count) < n:
        print("Only " + str(len(count)) + " numbers in file, sort amount updated")
        n = len(count)
    
    del count #only serves for updating count if necessary


    num_workers = 5
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()



    start_time = time.time()
    print("Starting overall sort @ " + str(start_time))

    numbers = read_and_split(input_file, n, num_workers) #splits list evenly based on worker count

    processes = []

    for workers in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for split in range(num_workers):
        input_queue.put(numbers[split]) #feeds the split lists to input queue for workers to take

    for split in range(num_workers):
        input_queue.put(None) #feeds the kill message to input queue

    sortedlists = []
    for i in range(num_workers):
        # print(i)
        sortedlists.append(output_queue.get()) #gets all the sorted lists from each worker thru the queue
        # print(sortedlists[-1])
    
    for p in processes:
        p.join() #waits until all workers are done

    # print(sortedlists)

    print("Recieved all " + str(num_workers) + " sorted lists @ " + str(time.time() - start_time) + ", merging them")

    finallist = []
    emptycount = 0
    while emptycount < len(sortedlists):
        emptycount = 0
        low_index = 0
        low_num = 999999999999
        for i in range(len(sortedlists)):
            if len(sortedlists[i]) == 0:
                emptycount += 1
                continue
            if sortedlists[i][0] < low_num:
                low_num = sortedlists[i][0]
                low_index = i
        if emptycount < len(sortedlists):
            finallist.append(low_num)
            sortedlists[low_index].pop(0)
        

    

    end_time = time.time()
    print("Time to distribute, sort, and merge " + str(n) + " numbers: " + str(end_time - start_time))
    print("Finished overall sort @ " + str(end_time))

    print("Writing sorted data to output file " + output_file)
    with open(output_file, 'w') as file:
        for number in finallist:
            file.write(f"{number}\n")

    
    print("Done")
