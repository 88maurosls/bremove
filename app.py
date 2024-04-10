import streamlit as st
import cv2
import numpy as np
from PIL import Image

def remove_background(image):
    # Converti l'immagine PIL in un array NumPy
    img_array = np.array(image)

    # Converti l'immagine da RGB a scala di grigi
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    # Applica una sogliatura per ottenere un'immagine binaria
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Trova i contorni nell'immagine binaria
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Crea una maschera per i contorni trovati
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Applica la maschera all'immagine originale per rimuovere lo sfondo
    result = cv2.bitwise_and(img_array, img_array, mask=mask)

    # Converti l'array NumPy risultante in un'immagine PIL
    result_image = Image.fromarray(result)

    return result_image

# Streamlit app
def main():
    st.title("Background Fashion Removal")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        input_image = Image.open(uploaded_file)

        # Process image
        output_image = remove_background(input_image)

        # Display processed image
        st.image(output_image, caption='Processed Image', use_column_width=True)

        # Button to download the processed image
        st.download_button(label='Download', data=output_image, file_name='output.png')

if __name__ == "__main__":
    main()
