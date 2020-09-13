import time

active_beds = []

while True:
    i = int(input("enter i"))
    j=int(input("enter j"))
    while (i <=j):
            bed = 'F' + '%d' % i
            print(bed)
            active_beds.append(bed)
            i = i + 1
            print(active_beds)

print("completed")
print(active_beds)
