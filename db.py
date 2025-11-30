# Este archivo tiene una sola función, crear y devolver una conexión a MYSQL

# la libreria pymysql sirve para conectar nuestro programa en python con una base de datos
# MYSQL
import pymysql

# creamos la función get_connection para poder crear la conexion y devolverla
# cada vez que en nuestro archivo app.py mandemos a llamar esta funcion, respondera de manera efectiva, enlazandonos a nuestra bd
def get_connection():
    print("conectandome con PyMySQL...")

    try:
        connection = pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="vehiculos",
            port=3306
        )
        # si funciona nuestra conexion, lanzamos un mensaje diciendo que si funcionó.
        print("Conexión establecida con PyMySQL")
        return connection

    except Exception as e:
        print("ERROR:", e)
        return None
