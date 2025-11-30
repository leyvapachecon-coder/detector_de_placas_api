# este es un arrchivo creado con la finalidad de saber si funciona la deteccion de placas
# (de python a sql) mediante placas "falsas", es decir, con pruebas unitarias e lugar de placas reales
import requests

API = "http://127.0.0.1:5000"

def probar_busqueda(placa):
    print(f"\n Probando placa: {placa}")
    url = f"{API}/vehiculos/{placa}"
    r = requests.get(url)

    print("RAW response:", r.text)

    try:
        print("JSON:", r.json())
    except:
        print("Error: No es JSON válido")

def probar_registro_vehiculo():
    print("\nRegistrando vehículo...")

    datos = {
        "placa": "ABC123",
        "marca": "Nissan",
        "modelo": "Versa",
        "anio": 2020,
        "propietario_id": 1
    }

    url = f"{API}/vehiculos"
    r = requests.post(url, json=datos)

    print("RAW response:", r.text)

    try:
        print("JSON:", r.json())
    except:
        print(" Error: No es JSON válido")

# pruebas unitarias
print("\nIniciando pruebas del API...")
probar_busqueda("ABC123")
probar_registro_vehiculo()
probar_busqueda("ABC123")
