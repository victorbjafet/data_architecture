import multiprocessing
import time
import dispy

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

    

def dworker(numbers):
    num_workers = 5
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    chunk_size = len(numbers) // num_workers
    remainder = len(numbers) % num_workers

    distributed = []
    index = 0
    for i in range(num_workers):
        extra = 1 if i < remainder else 0  # distribute remainder
        distributed.append(numbers[index:index + chunk_size + extra])
        index += chunk_size + extra 

    processes = []

    for workers in range(num_workers):
        from processfunc import pworker
        p = multiprocessing.Process(target=pworker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for split in range(num_workers):
        input_queue.put(distributed[split]) #feeds the split lists to input queue for workers to take

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

    # print("Recieved all " + str(num_workers) + " sorted lists @ " + str(time.time() - start_time) + ", merging them")

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
    
    return finallist
    
    





if __name__ == "__main__":
    # input_file = "data1.set"
    # output_file = "output.txt"

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


    start_time = time.time()
    print("Starting overall sort @ " + str(start_time))

    numbers = read_and_split(input_file, n, 30) #jobs usually all get sent to one node if number is 3, so make it a high number to actually distribute it

    nodes = ["10.0.0.20","10.0.0.30","10.0.0.40"]
    cluster = dispy.JobCluster(dworker, nodes=nodes, depends=["processfunc.py"])

    jobs = []
    sorted_lists = []
    for chunk in numbers:
        job = cluster.submit(chunk)
        jobs.append(job)

    cluster.wait()

    # print(jobs)

    for job in jobs:
        # print(str(job) + " working")
        job() # waits for job to finish and returns results
        if job.exception:
            print(job.exception)
        # print('%s executed job %s at %s with %s' % (host, job.id, job.start_time, n))
        sorted_lists.append(job.result)
    
    cluster.print_status()

    # print(sorted_lists)

    print("Combining lists from dispy nodes")

    finallist = []
    emptycount = 0
    while emptycount < len(sorted_lists):
        emptycount = 0
        low_index = 0
        low_num = 999999999999
        for i in range(len(sorted_lists)):
            if len(sorted_lists[i]) == 0:
                emptycount += 1
                continue
            if sorted_lists[i][0] < low_num:
                low_num = sorted_lists[i][0]
                low_index = i
        if emptycount < len(sorted_lists):
            finallist.append(low_num)
            sorted_lists[low_index].pop(0)

    

    end_time = time.time()
    print("Time to distribute, sort, and merge " + str(n) + " numbers: " + str(end_time - start_time))
    print("Finished overall sort @ " + str(end_time))

    print("Writing sorted data to output file " + output_file)
    with open(output_file, 'w') as file:
        for number in finallist:
            file.write(f"{number}\n")

    
    print("Done")
