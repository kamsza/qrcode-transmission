from pyzbar import pyzbar
import cv2
import base64
import os
import time

print("RECEIVER starts working")

list_of_indexes = []                    # read qrcodes indexes
missing_indexes = []                    # missing qrcodes indexes
map_with_data = {}

cap = cv2.VideoCapture("http://192.168.137.132:4747/video")             # ip and port taken from DroidCamApp

start_flag = True

i = 0

while True:

    i += 1
    if i > 100000:
        print("Time's up - transfer unsuccessful")

    # reading camera image
    ret, img = cap.read()

    if not ret:
        print("Could not read camera image")
        time.sleep(2)
        continue

    # decoding camera image
    decoded_qr = pyzbar.decode(img)

    if not decoded_qr:
        continue

    (index_str, _, rest) = decoded_qr[0].data.decode('utf-8').partition("/")
    (amount_str, _, data) = rest.partition("|")

    index, amount = int(index_str), int(amount_str)

    # starting time measurement on first loop step
    if start_flag:
        start_time = time.time()
        missing_indexes = list(range(0, amount))

    # if all codes are read - we finish
    if len(list_of_indexes) == amount:
        print("Reading finished!")
        break;

    # if we read the same index again
    if index in list_of_indexes:
        print("Again: " + str(index))
        continue;

    # save and print
    list_of_indexes.append(index)
    missing_indexes.remove(index)
    map_with_data[index] = data

    list_of_indexes.sort()

    os.system('cls')
    print("------------------------------------------------------------")
    print("GOT: ", list_of_indexes, "\nMISSING: ", missing_indexes)
    print("------------------------------------------------------------")

    start_flag = False

end_time = time.time()

return_file = bytes()

# merging read data into one variable (data must be sorted)
for key in sorted(map_with_data.keys()):
    return_file += base64.b64decode(map_with_data[key])

# exporting image
with open('../img/captured.png', 'wb') as f:
    f.write(return_file)

# closing credits
measured_time = end_time - start_time
data_size = len(return_file) / 1000
transfer_speed = data_size / measured_time

print("\n\n=================================================================")
print("Captured file saved as capture.png in img directory")
print("Transfer time: " + "{0:.2f}".format(round(measured_time, 2)) + "s")
print("Data size: " + "{0:.2f}".format(round(data_size, 2)) + "kB")
print("Data transfer: " + "{0:.2f}".format(round(transfer_speed, 2)) + "kB/s")
print("=================================================================\n\n")