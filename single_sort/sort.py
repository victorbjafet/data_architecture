import time

def read_numbers(file_path, n):
    with open(file_path, 'r') as file:
        numbers = [int(line.strip()) for _, line in zip(range(n), file)]
    return numbers

def bubble_sort(numbers, n):
    start_time = time.time()
    print("Starting sort")
    counter = 0
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
                swapped = True
        if not swapped:
            break
        if counter == 250:
            print(str(time.time() - start_time) + "s | " + str(i) + " sorted")
            counter = 0
        counter += 1

    end_time = time.time()
    print("Time to sort " + str(n) +" numbers: " + str(end_time - start_time))
    return numbers

def write_numbers(file_path, numbers):
    print("Writing sorted data to output file...")
    with open(file_path, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

def main(input_file, output_file, n):
    numbers = read_numbers(input_file, n)

    if len(numbers) < n:
        print("Only " + str(len(numbers)) + " numbers in file, sort amount updated")
        n = len(numbers)

    sorted_numbers = bubble_sort(numbers, n)

    write_numbers(output_file, sorted_numbers)

    print("Done")


if __name__ == "__main__":
    input_file = "data1.set"
    output_file = "output.txt"
    try:
        n = int(input("Number of ints to sort: "))
    except:
        print("Not an integer")
        raise ValueError

    main(input_file, output_file, n)
