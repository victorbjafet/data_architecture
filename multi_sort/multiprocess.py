import multiprocessing
import time

def worker(queueobj):
    while True:
        message = queueobj.get()
        if message == "exit":
            break
        print("worker: " + multiprocessing.current_process().name + " | received: " + message)
        time.sleep(0.1)


if __name__ == "__main__":
    workercount = 5  # Number of worker processes
    messagecount = 50  # Number of messages to send to the queue

    queue = multiprocessing.Queue()
    pool = multiprocessing.Pool(workercount, worker, (queue,))

    for num in range(messagecount): # send messages
        queue.put("msg " + str(num+1))

    for i in range(workercount): #stop workers
        queue.put("exit")

    pool.close()
    pool.join()
