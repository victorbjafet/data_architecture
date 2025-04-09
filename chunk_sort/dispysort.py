import multiprocessing
import time
import dispy
import os


def dworker(filename, chunk_number, chunk_size, use_multiprocessing):
    from chunking import get_chunk
    numbers = get_chunk(filename, chunk_number, chunk_size, 0)[1]
    #raise Exception(str(numbers))


    if use_multiprocessing:
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
        
        with open("/home/orangepi/nfsshare/sorted_chunks/sorted_chunk_" + str(chunk_number) + ".txt", 'w') as file:
            for number in finallist:
                file.write(f"{number}\n")

        return chunk_number        


    
    else:
        n = len(numbers)
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1): #only iterates thru uns
                if numbers[j] > numbers[j + 1]:
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                    swapped = True
            if not swapped:
                break
    
        with open("/home/orangepi/nfsshare/sorted_chunks/sorted_chunk_" + str(chunk_number) + ".txt", 'w') as file:
            for number in numbers:
                file.write(f"{number}\n")

        return chunk_number        




if __name__ == "__main__":
    from chunking import get_chunk_indices
    # input_file = "data1.set"
    # output_file = "output.txt"

    input_file = "/home/orangepi/nfsshare/datasets/data1.set"
    output_file = "/home/orangepi/nfsshare/outputs/output.txt"

    use_multiprocessing = False #probably broken as of rn

    try:
        chunk_count = int(input("Number of chunks to sort: "))
    except:
        print("Not an integer")
        raise ValueError

    try:
        chunk_size = int(input("Max number of bytes per chunk: "))
    except:
        print("Not an integer")
        raise ValueError

    try:
        indices = get_chunk_indices(input_file, chunk_count, chunk_size, 0)
        print("Reading " + str(indices[1]) + " bytes total")
    except:
        print("Reading more bytes than the file has (" + str(os.path.getsize(input_file)) + " bytes)")
        print("Exiting program, try again")
        exit(1)



    start_time = time.time()
    print("Starting overall sort @ " + str(start_time))
    nodes = ['10.0.0.10','10.0.0.20','10.0.0.30','10.0.0.40']
    cluster = dispy.JobCluster(dworker, nodes=nodes, depends=["processfunc.py","chunking.py"])

    jobs = []
    sorted_lists = []
    for i in range(chunk_count):
        job = cluster.submit(input_file, i + 1, chunk_size, use_multiprocessing)
        jobs.append(job)

    #cluster.wait()
    with open("job_outputs.txt", "w") as file:
        jobs_done = False
        last_chunk = 0
        while not jobs_done:
            length = len(jobs)
            #print("not jobs_done")
            if not length:
            #jobs_done = True
                break
            for i in range(length - 1, -1, -1):
                job = jobs[i]
            #print(job.status)
            if job.exception:
                print(job.exception)
                file.write(job.exception)
            if job.status == dispy.DispyJob.Finished:
                file.write(f"Job {job.id} is complete, chunk {job.result} should be done\n")
                print(f"Job {job.id} is complete, chunk {job.result} should be done")
                #process file early here
                if last_chunk == 0:
                    last_chunk = job.result
                else:
                    pass
                    #with open("/home/orangepi/nfsshare/sorted_chunks/sorted_chunk_" + str(last_chunk) + ".txt", 'r') as chunk1, open("/home/orangepi/nfsshare/sorted_chunks/sorted_chunk_" + str(job.result) + ".txt", 'r') as chunk2, open("/home/orangepi/nfsshare/sorted_chunks/layer_2_sorted_chunk_" + str(last_chunk) + ".txt", 'w'): #last file in list should be the one we r writing to
                    #   pass #ill deal w this later lol 
                jobs.pop(i)
            elif job.status == dispy.DispyJob.Cancelled:
                file.write(f"Job {job.id} was cancelled\n")
                jobs.pop(i)
            elif job.status == dispy.DispyJob.Terminated:
                file.write(f"Job {job.id} was terminated\n")
                jobs.pop(i)
            elif job.status == dispy.DispyJob.Abandoned:
                file.write(f"Job {job.id} was abandoned\n")
                jobs.pop(i)




    #okay so the plan is
    #comment the cluster.wait above so that i can start processing jobs as they come in
    #probably try to find a way to process jobs as they come in 
    #not just in order of when they were appended
    #then pretty much combine each job output file one by one, writing to an output file each time to preserve memory
    #and then gradually keep combining each file until done
    #need to decide whether ill do a merge sort where i combine two job files at a time and then go from there
    #or if ill just keep doing each job to a single file that constantly grows
    #either way i also need to add some sort of memory overflow protection
    #each node has 1gb of memory so i gotta try and add some protection that
    #stops it from trying to take more (i think it causes a crash)
    #also gotta balance jobs between nodes cuz everything is being sent to node2
    #for whatever reason
    #and i can try and make the nodes wait to read a file and execute a job
    #only once there is enough memory free, allowing sending a million jobs
    #but preventing memory overflow





    # print(jobs)

    #for job in jobs:
    #    # print(str(job) + " working")
    #    job() # waits for job to finish and returns results
    #    if job.exception:
    #        print(job.exception)
    #    # print('%s executed job %s at %s with %s' % (host, job.id, job.start_time, n))
    #    #sorted_lists.append(job.result)
    
    cluster.print_status()

    # print(sorted_lists)

    print("Combining lists from dispy nodes")

    for i in range(chunk_count):
        filelist = []
        try:
            dispy_output_file = "/home/orangepi/nfsshare/sorted_chunks/sorted_chunk_" + str(i + 1) + ".txt"
            #raise Exception(dispy_output_file)
            with open(dispy_output_file, "r") as file:
                for number in file:
                    filelist.append(int(number.strip()))
            sorted_lists.append(filelist)
        except Exception as e:
            raise Exception(e)
            #print("chunk file " + str(i + 1) + " is missing")
            #raise FileNotFoundError("dispynode issue")

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
    #print(finallist)
    print("Time to distribute, sort, and merge " + str(chunk_count) + " chunks of size " + str(chunk_size) + ": " + str(end_time - start_time))
    print("In total, processed " + str(get_chunk_indices(input_file, chunk_count, chunk_size, 0)[1]) + " bytes")
    print("Finished overall sort @ " + str(end_time))

    print("Writing sorted data to output file " + output_file)
    with open(output_file, 'w') as file:
        for number in finallist:
            file.write(f"{number}\n")

    print("Done")
