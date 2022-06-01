import base64

def encode_file_to_base64(file):
    data = file.read()
    file_base64 = str(base64.b64encode(data))
    encoded = file_base64.split("'")[1]
    return encoded