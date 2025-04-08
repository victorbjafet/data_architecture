file1 = "/home/orangepi/nfsshare/data1.set_validate_1000.txt"
file2 = "/home/orangepi/nfsshare/data2.set_validate_1000.txt"

output_file = "/home/orangepi/nfsshare/output.txt"

print("Merging sorted files " + file1 + " and " + file2 + " to output file " + output_file)

sortedlists = [[],[]]

with open(file1, 'r') as file:
    for line in file:
        line = line.strip()
        sortedlists[0].append(int(line))

with open(file2, 'r') as file:
    for line in file:
        line = line.strip()
        sortedlists[1].append(int(line))

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

with open(output_file, 'w') as file:
    for number in finallist:
        file.write(f"{number}\n")


print("Done")
