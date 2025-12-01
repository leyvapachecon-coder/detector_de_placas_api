# Este archivo es la magia de nuestro proyecto, pues aqui logramos hacer la deteccion de nuestras placas vehiculares
# a partir de una imagen utilizando procesamientos de imagenes, tales como openCV y OCR (Tesseract)

# CV2 es una libreria de openCV que se utiliza para el procesamiento de imagenes 
import cv2
# pytesseract viene siendo el enlace entre python y el OCR tesseract
import pytesseract
# re es una libreria para expresiones regulares, y nos sirve para poder buscar nuestra placa dentro del texto detectado
import re

# aquí indicamos a python donde está ubicado e instalado pytesseract en nuestra computadora
# cabe resaltar que si se quiere utilizar pytesseract, vimos un video de como instalarlo, por lo que la tarea de cada uno es verlo
# e instalarlo, por ende, indicarle a python donde lo guardaste, yo decidi guardarlo en este PATH. ENLACE AL VIDEO -> https://www.youtube.com/watch?v=sjmyHP-_h8Q&t=213s
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# este metodo va a ser nuestro detector de placas. a partir de aquí, decidimos usar procesadores de imagenes (openCV y tesseract) debido a que no tenemos el conocimiento
# de como entrenar a un modelo de vision artificial (tal como YOlO)
# lo que haremos primero es procesar nuestra imagen (con openCV) para luego pasar esa imagen ya procesada a tesseract (OCR)
def detectar_placa(imagen_path):
    # aqui lo que hacemos es intentar abrir la iamgen, si regresa NONE, la imagen no existe 
    imagen = cv2.imread(imagen_path)
    if imagen is None:
        print("Error: no se pudo abrir la imagen.")
        return None, ""
    
   # aqui lo que hacemos es agregar bordes blancos, ya que tesseract funciona mejor cuando la placa tiene un margen blanco alrededor
    # por ende, esto mejora muchisimo la deteccion
    imagen = cv2.copyMakeBorder(
        imagen, top=10, bottom=10, left=20, right=25,
        borderType=cv2.BORDER_CONSTANT, value=[255,255,255]
    )

    # aqui lo que hacemos es agregar bordes blancos, ya que tesseract funciona mejor cuando la placa tiene un margen blanco alrededor
    # por ende, esto mejora muchisimo la deteccion
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    # aplicamos un suavizador, esto con el fin de reducir el ruido y evitar que tesseract confunda el ruido con texto 
    gris = cv2.GaussianBlur(gris, (3,3), 0)

    # aqui aplicamos un contraste de las letras debiles para poder mejorar la lectura en imagenes oscuras o muy brillosas
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    gris = clahe.apply(gris)

    # en la umbralización, creamos una imagen en negro y blanco, diciendo que las letras son negras y el fondo sea blanco
    # OTSU es un algoritmo que calcula automaticamente el mejor umbral posible
    _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # aqui lo quehacemos es dilatar la imagen para poder engrosar los caracteres, esto lo hacemos para ayudar a tesseract a distinguir las letras pequeñas o debiles
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,3))
    umbral = cv2.dilate(umbral, kernel, iterations=1)

    # esto es mas que nada depuracion, para saber que imagen le estoy enviando al OCR
    cv2.imwrite("debug_umbral.png", umbral)

    # aqui configuramos al OCR, y usamos Psm 8 para que tesseract analize la imagen como una sola palabra, lo cual es ideal para las placas
    config = "--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    # aqui tesseract intenta leer texto en la imagen preprocesada
    texto = pytesseract.image_to_string(umbral, config=config)

    print("RESULTADO DEL OCR:\n", texto)

     # esta expresion regular lo que hace es buscar patrones como "ABC123", "ABC-123" etc...
    patron = r"[A-Z]{3}-?\d{3}-?[A-Z]"
    placas = re.findall(patron, texto)

    # si se detecta la placa, regresamos la primera coincidencia 
    if placas:
        placa_detectada = placas[0].replace(" ", "").upper()
        print("Placa detectada:", placa_detectada)
        return placa_detectada, texto.strip()

    print("No se pudo detectar la placa.")
    return None, texto.strip()

# ejecutamos nuestro archivo principal para poder ver si funciona, en este caso le mandamos una imagen ya preprocesada para ver si funcionaba
# llamada "placas.jpg", todo esto con el fin de ver si funcionaba nuestro 
if __name__ == "__main__":
    placa, ocr = detectar_placa("placas.jpg")
    print("Placa detectada:", placa)
    print("OCR completo:\n", ocr)
