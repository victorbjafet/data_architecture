def pworker(input_queue, output_queue):
    import multiprocessing
    import time


    while True:
        numbers = input_queue.get()

        if numbers == None:
            print(multiprocessing.current_process().name + " killed")
            break #stop worker if no more to sort

        start_time = time.time()

        n = len(numbers)
        # print(multiprocessing.current_process().name + " started sorting " + str(n) + " numbers @ " + str(start_time))

        
        counter = 0
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if numbers[j] > numbers[j + 1]:
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                    swapped = True
            if not swapped:
                break
            if counter == n//20: #change this number to change print frequency
                # print(multiprocessing.current_process().name + " | " +str(time.time() - start_time) + "s | " + str(i) + " sorted")
                counter = 0
            counter += 1
        
        # print(multiprocessing.current_process().name + " finished sorting " + str(n) + " numbers @ " + str(time.time() - start_time))
        output_queue.put(numbers)
