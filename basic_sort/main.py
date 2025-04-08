targetfile = "list1.txt"

with open(targetfile, "r+") as file:
    data = file.readlines()
    for i in range(len(data)):
        data[i] = int(data[i].strip())

datasorted = sorted(data)

change = True
while change != False:
    i = 0
    change = False
    while i < len(data) - 1:
        if data[i] > data[i + 1]:
            temp = data[i]
            data[i] = data[i + 1]
            data[i + 1] = temp
            change = True
        i += 1

print(data) 
print("Correct: ", end = "")
print(datasorted == data)