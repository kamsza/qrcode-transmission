import base64
import qrcode
import math

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)


# Function opens chosen file, divides it into chunks, generates qr codes and save them as .png files
# in qrcodes directory
def generate(file_path):
    block_size = 820      # max 2953
                          # required: block_size % 4 = 0

    with open(file_path, "rb") as img_file:
        img_read = base64.b64encode(img_file.read())
        img_string = img_read.decode('utf-8')

    list_of_chunks = _chunks(img_string, block_size)

    for i in range(len(list_of_chunks)):
        qr.add_data(list_of_chunks[i])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("../qrcodes/" + str(i) + ".png")
        qr.clear()


# Function divides given file into chunks, that will be represented as separate qr codes
def _chunks(data, chunk_len):
    chunks_num = math.ceil(len(data) / chunk_len)
    if chunks_num > 256:
        print("Exceeded max chunks number value. Max value: 256, current value: " + str(chunks_num))

    return [str(i//chunk_len) + '/' + str(chunks_num) + '|' + data[i:i + chunk_len] for i in range(0, len(data), chunk_len)]
