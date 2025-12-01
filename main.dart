import 'dart:convert'; // esto sirve para convertir datos JSON del servidor
import 'dart:io'; // esto lo usamos para manejar archivos (en este caso la imagen tomada)

import 'package:flutter/material.dart'; // Widgets y UI de Flutter
import 'package:image_picker/image_picker.dart'; // Para abrir la cámara (de este caso nuestro celular)
import 'package:http/http.dart' as http; // Para enviar la imagen que tomemos de nuestro celular al servidor
import 'dart:async'; // Para manejar Future y timeout en caso de que falle o tarde el sistema en enviar la imagen al servidor

// Esto viene siendo nuestra URL de nuestro FLASK (que viene siendo la ruta detectar_vehiculo)
const String SERVER_URL = 'http://192.168.1.70:5000/detectar_vehiculo'; // ruta de nuestro archivo app.py, donde mandaremos la imagen y el OCR hara su trabajo

void main() {
  runApp(const MyApp()); // aquí iniciamos la aplicación Flutter
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Configuraciónes generales de nuestra app
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Detector de Placas',
      home: const HomePage(), // aqui ponemos la página principal de nuestra app
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {

  File? _imagen;            // Guardamos la foto tomada por la cámara
  bool _cargando = false;   // Indicamos si estamos enviando la imagen al servidor
  String _resultado = '';   // Texto con la placa detectada y OCR
  Map<String, dynamic>? _propietario; // ponemos los datos del propietario (si existen)

  final ImagePicker _picker = ImagePicker(); // Control para la cámara del celular

  // este método lo creamos para tomar una foto con la cámara
  Future<void> _tomarFoto() async {
    try {
      final XFile? foto = await _picker.pickImage(source: ImageSource.camera);
      if (foto == null) return; // aqui decimos que el usuario cancelo la toma de la foto

      // aqui actualizamos el estado
      setState(() {
        _imagen = File(foto.path);
        _resultado = '';
        _propietario = null; // Limpiamos los datos al tomar nueva foto, por si no nos gusto la que tomamos
      });

      print("Foto tomada: ${foto.path}");
    } catch (e) {
      _mostrarMensaje('Error al abrir la cámara: $e');
    }
  }

  // Método para enviar la imagen al servidor Flask
  Future<void> _enviarImagen() async {
    if (_imagen == null) {
      _mostrarMensaje('Toma una foto primero');
      return;
    }

    setState(() {
      _cargando = true;
      _resultado = '';
      _propietario = null;
    });

    try {
      final uri = Uri.parse(SERVER_URL);
      final request = http.MultipartRequest('POST', uri);

      // aqui adjuntamos la imagen al request
      request.files.add(await http.MultipartFile.fromPath('imagen', _imagen!.path));

      // aqui nos queda esperar la respuesta del servidor
      final streamedResponse = await request.send().timeout(const Duration(seconds: 30));
      final resp = await http.Response.fromStream(streamedResponse);

      // Si el servidor respondió correctamente, mostramos la placa si se detecto o no
      if (resp.statusCode >= 200 && resp.statusCode < 300) {
        final map = json.decode(resp.body);

        final placa = map['placa_detectada'] ?? 'DESCONOCIDA';
        final ocrTexto = map['ocr'] ?? '---';

        setState(() => _resultado = 'Placa: $placa\nOCR: $ocrTexto');

        // aqui lo que hacemos es ver si el servidor devolvió el propietario
        if (map['data'] != null) {
          setState(() => _propietario = map['data']);
        } else {
          setState(() => _propietario = null);
        }

      } else {
        // si hay un error, mandamos: Error en el servidor Flask
        setState(() => _resultado = 'Error servidor: ${resp.statusCode} ${resp.reasonPhrase}');
      }

    } on SocketException {
      setState(() => _resultado = 'Error de conexión. Revisa la URL y la red.');
    } on Exception catch (e) {
      setState(() => _resultado = 'Error: $e');
    } finally {
      setState(() => _cargando = false); 
    }
  }

  // este es un método que sirve para mostrar mensajes en pantalla
  void _mostrarMensaje(String texto) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(texto)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detector de Placas'),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // esta es la sección donde se muestra la imagen tomada por el celular
            Expanded(
              child: Center(
                child: _imagen == null
                    ? const Text(
                        'No hay imagen\nPulsa "Tomar foto"',
                        textAlign: TextAlign.center,
                      )
                    : Image.file(_imagen!),
              ),
            ),

            if (_cargando) const LinearProgressIndicator(), 

            const SizedBox(height: 12),

            // aqui esta lo bueno, aqui mostramos el texto de los resultados (la placa y el resultado del OCR)
            Text(
              _resultado,
              style: const TextStyle(fontSize: 16),
            ),

            const SizedBox(height: 12),

            // Mostramos los datos del propietario
            if (_propietario != null) ...[
              Text('Propietario:',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Text('Nombre: ${_propietario!['propietario_nombre']}'),
              Text('Teléfono: ${_propietario!['telefono']}'),
              Text('Dirección: ${_propietario!['direccion']}'),
              const SizedBox(height: 12),
            ],

            //aqui esta el diseño, que viene siendo los botones de tomar foto y enviar
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _tomarFoto,
                    icon: const Icon(Icons.camera_alt),
                    label: const Text('Tomar foto'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _cargando ? null : _enviarImagen,
                    icon: const Icon(Icons.cloud_upload),
                    label: const Text('Enviar al servidor'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
