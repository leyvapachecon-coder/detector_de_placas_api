import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detectar_placa(imagen_path):

    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print("Error: no se pudo abrir la imagen.")
        return None, ""

    imagen = cv2.copyMakeBorder(
        imagen, top=10, bottom=10, left=20, right=25,
        borderType=cv2.BORDER_CONSTANT, value=[255,255,255]
    )

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    gris = cv2.GaussianBlur(gris, (3,3), 0)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gris = clahe.apply(gris)

    _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3))
    umbral = cv2.dilate(umbral, kernel, iterations=1)

    cv2.imwrite("debug_umbral.png", umbral)

    config = "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    texto = pytesseract.image_to_string(umbral, config=config)

    print("RESULTADO DEL OCR:\n", texto)

    # ===== REGEX MEJORADO =====
    # Detecta placas del tipo ABC-123-A y ABC123A
    patron = r"[A-Z]{3}-?\d{3}-?[A-Z]"
    placas = re.findall(patron, texto)

    if placas:
        # Normalizar (ej: ABC-123-A → ABC-123-A)
        placa_detectada = placas[0].replace(" ", "").upper()
        print("Placa detectada:", placa_detectada)
        return placa_detectada, texto.strip()

    print("No se pudo detectar la placa.")
    return None, texto.strip()


if __name__ == "__main__":
    placa, ocr = detectar_placa("placas.jpg")
    print("Placa detectada:", placa)
    print("OCR completo:\n", ocr)
