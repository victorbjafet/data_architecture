import time

def read_numbers(file_path, n):
    with open(file_path, 'r') as file:
        numbers = [int(line.strip()) for _, line in zip(range(n), file)]
    return numbers

def bubble_sort(numbers, n):
    start_time = time.time()
    print(f"Start sorting {n} numbers. Start time: {start_time}")

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                swapped = True
        if not swapped:
            break

        # Display progress every minute
        elapsed_time = time.time() - start_time
        if elapsed_time >= 60:
            print(f"Sorted through {i+1} numbers so far...")
            start_time = time.time()

    end_time = time.time()
    print(f"End sorting at {end_time}")

    return numbers

def write_numbers(file_path, numbers):
    with open(file_path, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

def main(input_file, output_file, n):
    start_time = time.time()

    # Read numbers
    numbers = read_numbers(input_file, n)

    # Sort numbers
    sorted_numbers = bubble_sort(numbers, n)

    # Write sorted numbers
    write_numbers(output_file, sorted_numbers)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time to read, sort, and write {n} numbers: {total_time:.2f} seconds.")

if __name__ == "__main__":
    input_file = "/home/orangepi/nfsshare/data1.set"
    n = 1000  # Start with 10,000 and increase until sorting exceeds 30 minutes
    output_file = "/home/orangepi/nfsshare/output.txt"

    main(input_file, output_file, n)

    # To find the largest N, incrementally increase n and rerun until time exceeds 1800 seconds (30 minutes).

