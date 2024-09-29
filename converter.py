import json
import cv2
import pytesseract

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_letter_soup_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen.")
        return []
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply w&b
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

    binary_image = cv2.bitwise_not(binary_image)

    cv2.imshow("a", binary_image)
    cv2.waitKey()

    custom_config = r'--oem 3 --psm 6'
    ocr_result = pytesseract.image_to_string(binary_image, config=custom_config)

    lines = ocr_result.splitlines()
    letter_soup = [''.join(line.replace(" ", "").upper()) for line in lines if line.strip() != '']

    return letter_soup

def extract_word_list_from_image(wordlist_image_path):
    image = cv2.imread(wordlist_image_path)
    if image is None:
        print("Error: No se pudo cargar la imagen de la lista de palabras.")
        return []
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV)

    custom_config = r'--oem 3 --psm 6'
    ocr_result = pytesseract.image_to_string(binary_image, config=custom_config)

    word_list = [word.strip().upper() for word in ocr_result.splitlines() if word.strip() != '']

    return word_list

def generate_soup_json(image_path, wordlist_image_path, json_file='soup.json'):
    soup = extract_letter_soup_from_image(image_path)
    word_list = extract_word_list_from_image(wordlist_image_path)

    if not soup:
        print("Error: No se pudo extraer la sopa de letras.")
        return

    soup_data = {
        "soup": soup,
        "words": word_list
    }

    with open(json_file, 'w') as outfile:
        json.dump(soup_data, outfile, indent=4)

    print(f'Sopa de letras generada y guardada en {json_file}')

if __name__ == "__main__":
    generate_soup_json('soup.png', 'wordlist.png')
