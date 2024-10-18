from PIL import Image
import numpy as np
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes

# Function to pad data to be a multiple of 8 bytes (block size for DES)
def pad(data):
    while len(data) % 8 != 0:
        data += b' '  # Padding with spaces
    return data



# Function to encrypt image
def encrypt_image(image_path, output_path, key):
    # Load the image
    img = Image.open(image_path)
    img_data = np.array(img)
    
    # Convert image to bytes
    img_bytes = img_data.tobytes()
    img_bytes = pad(img_bytes)  # Pad to multiple of 8 bytes
    
    # Create Triple DES cipher object
    cipher = DES3.new(key, DES3.MODE_ECB)
    
    # Encrypt the image bytes
    encrypted_img_bytes = cipher.encrypt(img_bytes)
    
    # Save encrypted image bytes as file
    with open(output_path, 'wb') as f:
        f.write(encrypted_img_bytes)
    
    print(f"Image encrypted and saved at {output_path}")

# Function to decrypt image
# Function to decrypt image
def decrypt_image(encrypted_image_path, output_path, key, original_shape):
    # Load the encrypted image bytes
    with open(encrypted_image_path, 'rb') as f:
        encrypted_img_bytes = f.read()
    
    # Create Triple DES cipher object
    cipher = DES3.new(key, DES3.MODE_ECB)
    
    # Decrypt the image bytes
    decrypted_img_bytes = cipher.decrypt(encrypted_img_bytes)
    
    # Convert bytes back to image data
    decrypted_img_data = np.frombuffer(decrypted_img_bytes, dtype=np.uint8).reshape(original_shape)
    
    # Convert the array back to an image
    decrypted_img = Image.fromarray(decrypted_img_data)
    
    # Convert to RGB if the mode is RGBA
    if decrypted_img.mode == 'RGBA':
        decrypted_img = decrypted_img.convert('RGB')
    
    # Save the decrypted image
    decrypted_img.save(output_path, 'PNG')

    
    print(f"Image decrypted and saved at {output_path}")


# Main program
if __name__ == "__main__":
    # Define paths
    input_image_path = 'input_image1.jpg'  # Input image
    encrypted_image_path = 'encrypted_image.des'  # Encrypted output file
    decrypted_image_path = 'decrypted_image.png'  # Decrypted output image

    # Generate a 24-byte (192 bits) Triple DES key
    key = DES3.adjust_key_parity(get_random_bytes(24))

    # Open the original image to get its shape (for reconstruction after decryption)
    original_image = Image.open(input_image_path)
    original_shape = np.array(original_image).shape

    # Encrypt the image
    encrypt_image(input_image_path, encrypted_image_path, key)

    # Decrypt the image
    decrypt_image(encrypted_image_path, decrypted_image_path, key, original_shape)
