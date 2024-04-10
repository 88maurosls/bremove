import streamlit as st
from PIL import Image
import numpy as np
import io
from u2net import detect

def process_image(input_image):
    """Process the input image to remove the background using U^2-Net."""
    # Convert PIL Image to numpy array
    input_array = np.array(input_image.convert('RGB'))
    
    # Detect the foreground mask
    result = detect(input_array)
    mask = (result > 0.5).astype(np.uint8) * 255  # Threshold adjusted here

    # Create a PIL Image from the numpy array
    mask_image = Image.fromarray(mask)

    # Prepare output image (composite the input with the mask)
    background = Image.new("RGB", input_image.size, (255, 255, 255))
    background.paste(input_image, mask=mask_image)
    return background

def main():
    st.title("Background Removal with U^2-Net")

    # File uploader allows user to add their own image
    uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg'])

    if uploaded_file is not None:
        input_image = Image.open(uploaded_file).convert('RGB')

        # Process image
        output_image = process_image(input_image)

        # Display processed image
        st.image(output_image, caption='Processed Image', use_column_width=True)

        # Save the processed image to a buffer
        buf = io.BytesIO()
        output_image.save(buf, format='PNG')
        byte_im = buf.getvalue()

        # Button to download the processed image
        st.download_button(label="Download Processed Image",
                           data=byte_im,
                           file_name='processed_image.png',
                           mime='image/png')

if __name__ == "__main__":
    main()
