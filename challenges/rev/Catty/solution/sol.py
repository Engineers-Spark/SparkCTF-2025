import os

PNG_HEADER = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

def xor_bytes(data, key):

    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def derive_xor_key(output_header):

    if len(output_header) != len(PNG_HEADER):
        raise ValueError("Output header must be 8 bytes long.")
    return xor_bytes(output_header, PNG_HEADER)

def xor_png_image(input_path, output_path):

    with open(input_path, "rb") as f:
        image_data = f.read()

    output_header = image_data[:8]
    xor_key = derive_xor_key(output_header)
    print(f"Derived XOR Key: {xor_key.hex()}")

    decrypted_data = xor_bytes(image_data, xor_key)

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

    print(f"Decrypted image saved to: {output_path}")

if __name__ == "__main__":

    input_image = "output.png"
    output_image = "decrypted_output.png"

    if not os.path.exists(input_image):
        print(f"Error: {input_image} does not exist.")
    else:
        xor_png_image(input_image, output_image)