from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import requests


def get_number_from_img():
    image = Image.open(r'Снимок экрана (952).png')

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    width, height = image.size

    # area = (450, 1317, width - 2070, height - 250)
    area = (10, 1450, width - 2490, height - 90)

    cropped_img = image.crop(area)

    sharpened_image = cropped_img.filter(ImageFilter.SHARPEN)

    custom_config = r'--oem 3 --psm 6'

    enhancer = ImageEnhance.Contrast(sharpened_image)

    enhanced_image = enhancer.enhance(2.0)

    enhanced_image.save(r'Снимок экрана (953).png')

    enhanced_image.show()

    text_1 = pytesseract.image_to_string(enhanced_image, config=custom_config)

    return text_1


def get_number_from_img_v2(api_key):
    image = Image.open(r'screenshot.png')

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    width, height = image.size

    # area = (10, 1350, width - 1070, height)
    area = (1908, 1044, width - 620, height - 520)
    # area = (92, 1480, width - 2450, height - 98)

    cropped_img = image.crop(area)

    sharpened_image = cropped_img.filter(ImageFilter.SHARPEN)

    enhancer = ImageEnhance.Contrast(sharpened_image)

    enhanced_image = enhancer.enhance(2.0)

    enhanced_image.show()

    enhanced_image.save(r'save_screen.png')

    image_data = open(r'save_screen.png', 'rb').read()

    # Отправка POST-запроса на OCR.space API
    payload = {
        'apikey': api_key,
        'language': 'eng',
        'isOverlayRequired': False,  # Не требуется наложение текста на изображение
        'detectOrientation': True,  # Автоматическое определение ориентации текста
        'scale': True,  # Масштабирование изображения
        'filetype': 'png',  # Формат изображения
        'OCREngine': 2
    }

    response = requests.post('https://api.ocr.space/parse/image', files={'image': image_data}, data=payload)
    number = response.json()['ParsedResults'][0]['ParsedText']

    return number


print(get_number_from_img_v2('K89172719188957'))
