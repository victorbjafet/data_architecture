if __name__ == "__main__":
    filename = 'data1.set'
    
    try:
        n = int(input("Enter the number of integers to read: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer for the count.")
    
    integers = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                try:
                    number = int(line.strip())
                    integers.append(number)
                except ValueError:
                    print(f"Skipping invalid integer: {line.strip()}")
                if len(integers) == n:
                    break
    
    sorted_numbers = sorted(integers)

    with open(filename + "_validate_" + str(n) + ".txt", 'w') as file:
        for number in sorted_numbers:
            file.write(f"{number}\n")