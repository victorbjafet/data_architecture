import time

targetfile = "data1.set"

outputfile = "output.txt"

try:
    n = int(input("Number of ints to sort: "))
except:
    print("Not an integer")
    raise ValueError

with open(targetfile, "r+") as file:
    data = [int(line.strip()) for _, line in zip(range(n), file)]

if len(data) < n:
    print("Only " + str(len(data)) + " numbers in file, sort amount updated")
    n = len(data)

print("Starting sort")

starttime = time.time()

change = True
passes = 0
while change != False:
    change = False
    for i in range(n - passes - 1):
        if data[i] > data[i + 1]:
            data[i], data[i + 1] = data[i + 1], data[i]
            change = True
    passes += 1
    if passes % 250 == 0:
        print(str(time.time() - starttime) + "s | " + str(passes) + " sorted")


print("Time to sort " + str(n) +" numbers: " + str(time.time() - starttime))
print("Writing sorted data to output file...")

with open(outputfile, "w+") as file:
    for num in data:
        file.write(f"{num}\n")

print("Done")