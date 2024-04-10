import streamlit as st
from rembg import remove
from PIL import Image

def process_image(input_image):
    output_image = remove(input_image)
    return output_image

# Streamlit app
def main():
    st.title("Frenz's Background Fashion Removal")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        input_image = Image.open(uploaded_file)

        # Process image
        output_image = process_image(input_image)

        # Display processed image
        st.image(output_image, caption='Processed Image', use_column_width=True)

        # Button to download the processed image
        output_path = 'removed.png'
        output_image.save(output_path)
        st.download_button(label='Download', data=open(output_path, 'rb').read(), file_name='output.png')

if __name__ == "__main__":
    main()
