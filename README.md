# detector_de_placas_api
en este repositorio encontraras todo lo necesario para poder crear tu primer detector de placas en una aplicacion movil, por favor, siga las instrucciones que se le den para poder instalar todo lo necesario y poder ejecutar el proyecto correctamente.

Favor de instalar las siguientes librerias necesarias para poder correr el codigo:
pip install flask
pip install flask-cors
pip install pymysql
pip install opencv-python
para poder instalar tesseract tiene que ser manualmente, nosotros lo hicimos con un video de youtube -> https://www.youtube.com/watch?v=sjmyHP-_h8Q&t=213s
pip install pytesseract
pip install pillow

y como dato extra pero no menos importante, usamos la versión 3.10 de python, ya que algunas librerías como tesseract, no nos permitían usarlas en la versión 3.13, asi que, por el momento usamos la versión 3.10.

Guía para descargar flutter en VS CODE:
Para descargar flutter tuvimos que hacerlo manual, mediante este video -> https://www.youtube.com/watch?v=BTubOBvfEUE
Si todo esta correcto con la instalacion, dirijase hacia su CDM, y ejecute el siguiente comando: "flutter doctor", dicho comando le dira si todo esta en orden o si le falto algo por instalar

una vez descargado flutter, dirijase a: Android -> app -> main -> res -> xml, dentro de esa extension llamada xml, encontrara un archivo llamado "androidManifest.xml", dentro de ese archivo coloque lo siguiente:
dentro de la etiqueta "manifest" (justo al inicio) -> uses-permission android:name="android.permission.CAMERA"/>
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>
    <uses-permission android:name="android.permission.INTERNET"/> que basicamente son algunos permisos que tenemos que dar para poder tomar foto, conexiones etc, todo desde nuestro celular.
    y dentro de la etiqueta "aplication", coloque lo siguiente:
        android:label="detector_placas"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:networkSecurityConfig="@xml/network_security_config"
        android:usesCleartextTraffic="true" 

Para poder crear la interfaz gráfica y la logica de conexion de nuestra api, dirijase hacia "lib/" y dentro de esa carpeta se encuentra el archivo "main..dart", donde irá toda la logica de la api (conexion e interfaz).

Por ultimo, dentro del archivo llamado ""pubspec.yaml, dirijase hacia donde dice "dependencies" y "flutter" va a colocar debajo de eso lo siguiente:
  sdk: flutter
  image_picker: ^1.0.7
  http: ^1.2.1
  *nota importante* -> asegurese de colocar el "sdk: flutter" debajo de flutter DOS ESPACIOS A LA DERECHA, y lo demas ALINEADO CON FLUTTER, ya que si no lo hace, le marcaría error.

  Para las pruebas en celular, tiene que configurarlo en modo desarrollador, para poder correr la aplicacion flutter, para eso, haga lo siguiente:
  - dirijase a configuraciones -> acerca del telefono -> compilacion, cuando encuentre esa palabra, presionela 7 veces hasta que le diga que ya es deasarrollador.
  - lo siguiente seria irse a configuraciones -> sistema y actualizaciones -> opciones de desarrollador -> y active la opcion de "Depuracion USB"
  - los iguiente seria ya la prueba, para eso, conecte su celular a su computadora mediante un cable (preferiblemente el de su cargador) y dele permisos al celular (transferencia de           archivos, depuracion usb) y su celular ya estaria listo para poder correr la aplicacion flutter
  - para ver si todo esta en orden y si su celular esta listo para poder depurar la aplicacion, dirijase a su CDM y coloque el siguiente comando:"flutter devices" y si su dispositivo          aparece ahi, todo esta en orden y correctamente instalado listo para poder correr la aplicacion.

 - si quiere correr la aplicacion, dirijase al apartado donde tiene abierto el flutter, en consola ponga el siguiente comando "flutter run", y dele los permisos al celular para poder correr la aplicacion, y se abrira inmediatamente
 - como nota extra en dado caso que no funcione el envio de la foto al servidor, tenga en cuenta que el cel y la computadora tienen que estar en la misma conexion de internet, para eso, dirijase a CDM y coloque el siguiente comando "ipconfig" y esa red tiene que estar conectada con su cel. en el celular, dirijase a wifi, y entre a su conexion a internet y verifique que todo este sincronizado, y ya deberia de funcionar el envio al servidor.
   
  !exito¡

