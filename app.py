# este archivo es el corazón del proyecto, ya que nos servirá para crear,controlar
# y exponer nuestra API, donde conectaremos nuestra base de datos y usaremos esos datos para
# la deteccion de las placas que mandemos al servidor

# la libreria flask nos ayudara a crear nuestra API, mientras que con request leeremos los datos
# y responderemos mediante un formato JSON
from flask import Flask, request, jsonify
# cors nos permite hacer peticiones desde apps externas, en etse caso como usaremos flutter, nos serivra
# para poder crear peticiones.
from flask_cors import CORS
# desde mi archivo db (donde hago mi conexion a base de datos),  utilizare la funcion get_connection para poder 
# conectarme a mysql
from db import get_connection
# necesitamos de un driver para poder ejecutar queries MYSQL
import pymysql
# desde mi archivo detector (donde estara mi lógica de detección de placas), importo la función "detectar placas"
# (mi función OCR) donde detectaremos las placas mediante imagenes
from detector import detectar_placa
# con os manejamos archivos en carpetas
import os

# aqui lo que hacemos es crear nuestra aplicación FLASK, y por ende, activamos CORS para poder permitir hacer peticiones
# desde el frontend (flutter en nuestro caso)
app = Flask(__name__)
CORS(app)

# creamos una carpeta temporal llamada uploads, ya que las imagenes que sean enviadas por el usuario se guardarán temporalmente ahi.
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# esto es mas que nada un debug para ver que todo llegue correctamente y no haya problemas en un futuro.
@app.before_request
def log_request():
    print("\n=== PETICIÓN ENTRANTE ===")
    print("Método:", request.method)
    print("Ruta:", request.path)
    print("Archivos recibidos:", request.files)
    print("Form data:", request.form)
    print("Headers:", request.headers)

# aqui lo que hacemos es saber si nuestro servidor esta vivo, y lo que hicimos fue probarlo en computadora y celular para poder ver si nuestras
# conexiones eran correctas y estaban sincronizadas para poder trabajar juntas, y asi lo fue.
@app.route("/")
def home():
    return jsonify({"message": "API funcionando correctamente"})


# Rutas de propietarios
# aqui hago una parada para explicar que, a partir de esta ruta hasta la ruta "buscar por medio del GET", son rutas que usamos para poder comprobar que 
# la inserción y consulta de datos de nuestra base de datos funciona correctamente desde nuestra API.
# asi que si gustan corroborar la funcionalidad de esta API, recomendamos hacer un tipo debug con todas estas rutas.
@app.route("/propietarios", methods=["GET"])
def listar_propietarios():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, nombre, telefono, direccion FROM propietarios")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/propietarios", methods=["POST"])
def registrar_propietario():
    datos = request.json
    nombre = datos.get("nombre")
    telefono = datos.get("telefono")
    direccion = datos.get("direccion")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO propietarios (nombre, telefono, direccion)
            VALUES (%s, %s, %s)
        """, (nombre, telefono, direccion))
        conn.commit()
        respuesta = {"status": "ok", "mensaje": "Propietario registrado"}
    except Exception as e:
        respuesta = {"status": "error", "detalle": str(e)}
    cursor.close()
    conn.close()
    return jsonify(respuesta)


# Rutas de vehiculos

@app.route("/vehiculos", methods=["GET"])
def listar_vehiculos():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT v.id, v.placa, v.marca, v.modelo, v.anio,
               p.id AS propietario_id, p.nombre AS propietario_nombre
        FROM vehiculos_p v
        JOIN propietarios p ON v.propietario_id = p.id
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/vehiculos", methods=["POST"])
def registrar_vehiculo():
    datos = request.json
    placa = datos.get("placa")
    marca = datos.get("marca")
    modelo = datos.get("modelo")
    anio = datos.get("anio")
    propietario_id = datos.get("propietario_id")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vehiculos_p (placa, marca, modelo, anio, propietario_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (placa, marca, modelo, anio, propietario_id))
        conn.commit()
        respuesta = {"status": "ok", "mensaje": "Vehículo registrado"}
    except Exception as e:
        respuesta = {"status": "error", "detalle": str(e)}
    cursor.close()
    conn.close()
    return jsonify(respuesta)


# Rutas de busqueda por placa

@app.route("/vehiculos/<placa>", methods=["GET"])
def buscar_vehiculo_por_url(placa):
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT v.id, v.placa, v.marca, v.modelo, v.anio,
               p.id AS propietario_id, p.nombre AS propietario_nombre,
               p.telefono, p.direccion
        FROM vehiculos_p v
        JOIN propietarios p ON v.propietario_id = p.id
        WHERE v.placa = %s
    """, (placa,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado:
        return jsonify({"status": "ok", "data": resultado})
    else:
        return jsonify({"status": "no_encontrado"})

@app.route("/buscar", methods=["GET"])
def buscar_vehiculo():
    placa = request.args.get("placa")
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT v.id, v.placa, v.marca, v.modelo, v.anio,
               p.id AS propietario_id, p.nombre AS propietario_nombre, 
               p.telefono, p.direccion
        FROM vehiculos_p v
        JOIN propietarios p ON v.propietario_id = p.id
        WHERE v.placa = %s
    """, (placa,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    if resultado:
        return jsonify({"status": "ok", "data": resultado})
    else:
        return jsonify({"status": "no_encontrado"})


# Ruta detectar vehiculo
# Esta es la ruta estrella, la que nos permite recibir una foto del vehículo, detectar la placa y poder hacer el OCR, para que
# podamos buscar en nuestra base de datos y poder devolver la informacion del propietario.
@app.route("/detectar_vehiculo", methods=["POST"])
def detectar_vehiculo():

    # verificamos que nuestra imagen llegue
    if 'imagen' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    #si llega, la guardamos
    archivo = request.files['imagen']
    ruta_imagen = os.path.join(UPLOAD_FOLDER, archivo.filename)
    archivo.save(ruta_imagen)

    # Detectamos la placa y se procesa el OCR completo
    # lo que nos devuelve el "detectar_placa" es -> la placa detectada y todo el texto OCR de la imagen
    placa, texto_ocr = detectar_placa(ruta_imagen)

    #aqui eliminamos la imagen temporal
    os.remove(ruta_imagen)

    # si no se detecto nada:
    if not placa:
        placa = "NO_DETECTADA"

    # aqui hacemos conexion a nuestra base de datos por medio del get_connection, y buscamos nuestra placa en MYSQL
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT v.id, v.placa, v.marca, v.modelo, v.anio,
               p.id AS propietario_id, p.nombre AS propietario_nombre,
               p.telefono, p.direccion
        FROM vehiculos_p v
        JOIN propietarios p ON v.propietario_id = p.id
        WHERE v.placa = %s
    """, (placa,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    # si se encontró o no, respondemos igual en un formato JSON
    return jsonify({
        "status": "ok",
        "placa_detectada": placa,
        "ocr": texto_ocr,
        "data": resultado
    })

# Fin de las rutas y ejecutamos el servidor
# ponemos host='0.0.0.0.' para poder darle acceso a nuestro celular 
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
