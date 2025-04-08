import random

filename = "list4.txt"

with open(filename, "w+") as file:
    for i in range(15):
        file.write(str(random.randrange(1,99999)) + "\n")